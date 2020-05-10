"""
Helios URLs for Election related stuff

Ben Adida (ben@adida.net)
"""

from django.urls import re_path

from helios.views import *

urlpatterns = [
    # election data that is cryptographically verified
    re_path(r'^$', one_election, name='one-election'),
    re_path(r'^election-abi$', one_election_abi, name='one-election-abi'),

    # metadata that need not be verified
    re_path(r'^meta$', one_election_meta, name='one-election-meta'),
    
    # edit election params
    re_path(r'^edit$', one_election_edit, name='one-election-edit'),
    re_path(r'^schedule$', one_election_schedule, name='one-election-schedule'),
    re_path(r'^archive$', one_election_archive, name='one-election-archive'),
    re_path(r'^copy$', one_election_copy, name='one-election-copy'),
    re_path(r'^freeze', one_election_freeze, name='one-election-freeze'),
    
    # deploy smart contract
    re_path(r'^deploy', one_election_deploy_contract, name='one-election-deploy-contract'),
    re_path(r'^final-freeze', one_election_final_freeze, name='one-election-final-freeze'),
    re_path(r'^ajax/contract$', deployed_contract, name='deployed-contract'),
    re_path(r'^ajax/question$', question_registered_to_contract, name='question-registered-to-contract'),
    re_path(r'^ajax/voters$', voters_added_to_contract, name='voters-added-to-contract'),
    re_path(r'^ajax/pubkey$', set_pubkey_transaction_contract, name='set-pubkey-transaction-contract'),

    # badge
    re_path(r'^badge$', election_badge, name='election-badge'),

    # adding trustees
    re_path(r'^trustees/$', list_trustees, name='list-trustees'),
    re_path(r'^trustees/view$', list_trustees_view, name='list-trustees-view'),
    re_path(r'^trustees/new$', new_trustee, name='new-trustee'),
    re_path(r'^trustees/add-helios$', new_trustee_helios, name='new-trustee-helios'),
    re_path(r'^trustees/delete$', delete_trustee, name='delete-trustee'),
    
    # trustee pages
    re_path(r'^trustees/(?P<trustee_uuid>[^/]+)/home$', trustee_home, name='trustee-home'),
    re_path(r'^trustees/(?P<trustee_uuid>[^/]+)/sendurl$', trustee_send_url, name='trustee-send-url'),
    re_path(r'^trustees/(?P<trustee_uuid>[^/]+)/keygenerator$', trustee_keygenerator, name='trustee-keygenerator'),
    re_path(r'^trustees/(?P<trustee_uuid>[^/]+)/check-sk$', trustee_check_sk, name='trustee-check-sk'),
    re_path(r'^trustees/(?P<trustee_uuid>[^/]+)/upload-pk$', trustee_upload_pk, name='trustee-upload-pk'),
    re_path(r'^trustees/(?P<trustee_uuid>[^/]+)/decrypt-and-prove$',trustee_decrypt_and_prove, name='trustee-decrypt-and-prove'),
    re_path(r'^trustees/(?P<trustee_uuid>[^/]+)/upload-decryption$', trustee_upload_decryption, name='trustee-upload-decryption'),
    
    # election voting-process actions
    re_path(r'^view$', one_election_view, name='one-election-view'),
    re_path(r'^result$', one_election_result, name='one-election-result'),
    re_path(r'^result_proof$', one_election_result_proof, name='one-election-result-proof'),
    # (r'^bboard$', one-election-bboard'),
    re_path(r'^audited_ballots/$', one_election_audited_ballots, name='one-election-audited-ballots'),

    # get randomness
    re_path(r'^get_randomness$', get_randomness, name='get-randomness'),

    # server-side encryption
    re_path(r'^encrypt_ballot$', encrypt_ballot, name='encrypt-ballot'),

    # construct election
    re_path(r'^questions$', one_election_questions, name='one-election-questions'),
    re_path(r'^set_reg$', one_election_set_reg, name='one-election-set-reg'),
    re_path(r'^set_featured$', one_election_set_featured, name='one-election-set-featured'),
    re_path(r'^save_questions$', one_election_save_questions, name='one-election-save-questions'),
    re_path(r'^register$', one_election_register, name='one-election-register'),
    re_path(r'^freeze$', one_election_freeze, name='one-election-freeze'), # includes freeze_2 as POST target
    
    # computing tally
    re_path(r'^compute_tally$', one_election_compute_tally, name='one-election-compute-tally'),
    re_path(r'^combine_decryptions$', combine_decryptions, name='combine-decryptions'),
    re_path(r'^release_result$', release_result, name='release-result'),
    
    # casting a ballot before we know who the voter is
    re_path(r'^cast$', one_election_cast, name='one-election-cast'),
    re_path(r'^cast_confirm$', one_election_cast_confirm, name='one-election-cast-confirm'),
    re_path(r'^password_voter_login$', password_voter_login, name='password-voter-login'),
    re_path(r'^cast_done$', one_election_cast_done, name='one-election-cast-done'),
    
    # post audited ballot
    re_path(r'^post_audited_ballot', post_audited_ballot, name='post-audited-ballot'),

    # managing voters
    re_path(r'^voters/$', voter_list, name='voter-list'),
    re_path(r'^voters/upload$', voters_upload, name='voters-upload'),
    re_path(r'^voters/upload-cancel$', voters_upload_cancel, name='voters-upload-cancel'),
    re_path(r'^voters/list$', voters_list_pretty, name='voters-list-pretty'),
    re_path(r'^voters/eligibility$', voters_eligibility, name='voters-eligibility'),
    re_path(r'^voters/email$', voters_email, name='voters-email'),
    re_path(r'^voters/(?P<voter_uuid>[^/]+)$', one_voter, name='one-voter'),
    re_path(r'^voters/(?P<voter_uuid>[^/]+)/delete$', voter_delete, name='voter-delete'),
    
    # ballots
    re_path(r'^ballots/$', ballot_list, name='ballot-list'),
    re_path(r'^ballots/(?P<voter_uuid>[^/]+)/all$', voter_votes, name='voter-votes'),
    re_path(r'^ballots/(?P<voter_uuid>[^/]+)/last$', voter_last_vote, name='voter-last-vote'),

]
