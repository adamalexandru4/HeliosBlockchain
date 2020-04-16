"""
Celery queued tasks for Helios

2010-08-01
ben@adida.net
"""

from celery import shared_task, task

from helios.models import *
from helios.view_utils import render_template_raw
from . import signals
import copy
from django.conf import settings
from Crypto import Random

from web3 import Web3, HTTPProvider

@shared_task()
def cast_vote_verify_and_store(cast_vote_id, election_contract_address, election_contract_abi, private_key, status_update_message=None, **kwargs):
    cast_vote = CastVote.objects.get(id = cast_vote_id)
    result = cast_vote.verify_and_store(election_contract_address, election_contract_abi, private_key)

    voter = cast_vote.voter
    election = voter.election
    user = voter.get_user()
    if result:
        # send the signal
        signals.vote_cast.send(sender=election, election=election, user=user, voter=voter, cast_vote=cast_vote)
        
        if status_update_message and user.can_update_status():
            from .views import get_election_url

            user.update_status(status_update_message)

    else:
        logger = cast_vote_verify_and_store.get_logger(**kwargs)
        logger.error("Failed to verify and store %d" % cast_vote_id)

    
@shared_task()
def voters_email(election_id, subject_template, body_template, extra_vars={},
                 voter_constraints_include=None, voter_constraints_exclude=None):
    """
    voter_constraints_include are conditions on including voters
    voter_constraints_exclude are conditions on excluding voters
    """
    print("Entering voters_email task")
    election = Election.objects.get(id = election_id)

    # select the right list of voters
    voters = election.voter_set.all()
    if voter_constraints_include:
        voters = voters.filter(**voter_constraints_include)
    if voter_constraints_exclude:
        voters = voters.exclude(**voter_constraints_exclude)

    for voter in voters:
        single_voter_email.delay(voter.uuid, subject_template, body_template, extra_vars)            

@shared_task()
def voters_notify(election_id, notification_template, extra_vars={}):
    election = Election.objects.get(id = election_id)
    for voter in election.voter_set.all():
        single_voter_notify.delay(voter.uuid, notification_template, extra_vars)

@shared_task()
def register_new_election_contract_blockchain(register_election_txn, private_key_bytes):

    private_key_bytes = bytes.fromhex(private_key_bytes)
    w3 = settings.WEB3

    try:
        signed_txn = w3.eth.account.sign_transaction(register_election_txn, private_key=private_key_bytes)
        w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)

    # let another thread to handle the receipt
    receipt_tx_register_election.delay(signed_txn.hash.hex())

@shared_task()
def receipt_tx_register_election(tx_hash):
    w3 = settings.WEB3
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print("Election with TX:" + tx_hash + " is registered after this transaction")
    print(dict(receipt))

@shared_task()
def single_voter_email(voter_uuid, subject_template, body_template, extra_vars={}):
    voter = Voter.objects.get(uuid = voter_uuid)

    the_vars = copy.copy(extra_vars)
    the_vars.update({'voter' : voter})

    subject = render_template_raw(None, subject_template, the_vars)
    body = render_template_raw(None, body_template, the_vars)

    voter.send_message(subject, body)

@shared_task()
def single_voter_notify(voter_uuid, notification_template, extra_vars={}):
    voter = Voter.objects.get(uuid = voter_uuid)

    the_vars = copy.copy(extra_vars)
    the_vars.update({'voter' : voter})

    notification = render_template_raw(None, notification_template, the_vars)

    voter.send_notification(notification)

@shared_task()
def election_compute_tally(election_id, election_contract_abi):
    Random.atfork()
    election = Election.objects.get(id = election_id)
    election.compute_tally(election_contract_abi)
    election_notify_admin.delay(election_id = election_id,
                                subject = "encrypted tally computed",
                                body = """
The encrypted tally for election %s has been computed.

--
Helios
""" % election.name)
                                
    if election.has_helios_trustee():
        tally_helios_decrypt.delay(election_id = election.id)

@shared_task()
def tally_helios_decrypt(election_id):
    Random.atfork()
    election = Election.objects.get(id = election_id)
    election.helios_trustee_decrypt()
    election_notify_admin.delay(election_id = election_id,
                                subject = 'Helios Decrypt',
                                body = """
Helios has decrypted its portion of the tally
for election %s.

--
Helios
""" % election.name)

@shared_task()
def voter_file_process(voter_file_id):
    print("entering voter_file_process")
    voter_file = VoterFile.objects.get(id = voter_file_id)
    voter_file.process()
    election_notify_admin.delay(election_id = voter_file.election.id, 
                                subject = 'voter file processed',
                                body = """
Your voter file upload for election %s
has been processed.

%s voters have been created.

--
Helios
""" % (voter_file.election.name, voter_file.num_voters))

@shared_task()
def election_notify_admin(election_id, subject, body):
    print("entering election_notify_adimin")
    election = Election.objects.get(id = election_id)
    election.admin.send_message(subject, body)
