export const question_markup = 
`
${QUESTIONS.map(
  (question, index) =>
  `
  <div class="card bg-secondary mb-3" id="q_view_${index}">
    <div class="card-header">
    <div class="row" style="max-width: unset; margin-left: 0px; margin-right: 0px;">
      <div class="col-md-9 col-sm-12" style="padding-left: 0px;">
        <h4 style="margin-bottom: 0px;">
          #${index + 1}. ${question.question}
        </h4>
      </div>
      
      ${ADMIN_P ?  
      `<div class="col-md-3 col-sm-12" style="padding-right: 0px;">
        <div class="d-flex justify-content-end">
          ${index > 0 ? `<a class="btn btn-sm btn-primary mr-1" href="javascript:question_move_up(${index})">MOVE UP</a>` : ``}
          <a class="btn btn-sm btn-info mr-1" href="javascript:question_edit(${index})">EDIT</a>
          <a class="btn btn-sm btn-danger" onclick="return confirm('Are you sure you want to remove this question?');" href="javascript:question_remove(${index})">DELETE</a>
        </div>
      </div>` : ``
      }
    </div>
    </div>
    <div class="card-body">
      <h4 class="card-title">(${question.choice_type}, select between ${question.min} and ${`${question.max != null}` ? `${question.max}` : `unlimited`} answers, result type ${question.result_type}.)</h4>
      <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
    </div>
  </div>


  <div id="q_view_${index}">
    <ul>
      ${question.answers.map(
        (answer, index) =>
        `
        <li> ${answer}
        ${`{question.answer_urls}[${index}]` ?
          `[<a target="_new" href="${question.answer_urls}[${index}]">more</a>]` : `''`
        }
        </li>
        `
      ).join('')}
    </ul>
  </div>
  <div id="q_edit_${index}" style="display:none;"> 
    <form id="question_edit_${index}_form" onsubmit="question_update(${index}, this); return false;" action="#">
      <p>
      <!--
        Type of Question:
        <select name="choice_type">
          <option selected>approval</option>
        </select>
      -->
      <input type="hidden" name="choice_type" value="approval" />
      <b>${index + 1}.</b> &nbsp;&nbsp;&nbsp;Select between &nbsp;&nbsp;
      <select name="min">
        <option selected>0</option>
        ${Array(20).fill().map( (item, idx) =>
          ` <option>${idx + 1}</option>`
          )}
      </select>

      &nbsp;&nbsp; and  &nbsp;&nbsp;

      <select name="max">
        <option>0</option>
        <option selected>1</option>

        ${Array(49).fill().map( (item, idx) =>
        ` <option>${idx + 2}</option>`
        )}

        <option value="">- (approval)</option>
      </select>

      &nbsp;&nbsp;
      answers.

      &nbsp;&nbsp;
      &nbsp;&nbsp;
      Result Type:&nbsp;
      <select name="result_type">
          <option selected>absolute</option>
          <option>relative</option>
      </select>

      </p>

      <table id="answer_table_${index}">
        <tbody>
          <tr><th colspan="2">Question:</th><td><input type="text" name="question" size="70" /></td></tr>
          <tr><th>&nbsp;</th><th>&nbsp;</th><th>&nbsp;</th></tr>
        </tbody>
        <tfoot>
          <tr><th colspan="2"></th><th><a href="javascript:add_answers(document.getElementById('answer_table_${index}'),5)">add 5 more answers</a></th></tr>
          <tr><td colspan="3"><input type="submit" value="update question" /> &nbsp; <input type="reset" value="cancel" onclick="question_edit_cancel(${index});" /></td></tr>
        </tfoot>

      </table>
    </form>
  </div>
`
).join('')}
${QUESTIONS.length == 0 ? `no questions yet` : ''}
${ADMIN_P ?
`
  <h4>Add a Question:</h4>
  <form id="question_form" onsubmit="question_add(this); return false;" action="#">
    <p>
    <!--
      Type of Question:
      <select name="choice_type">
        <option selected>approval</option>
      </select>
    -->
    <input type="hidden" name="choice_type" value="approval" />
    &nbsp;&nbsp;&nbsp;Select between &nbsp;&nbsp;
    <select name="min">
        <option selected>0</option>
        ${Array(20).fill().map( (item, idx) =>
          ` <option>${idx + 1}</option>`
          )}
    </select>

    &nbsp;&nbsp; and  &nbsp;&nbsp;

    <select name="max">
        <option>0</option>
        <option selected>1</option>

        ${Array(49).fill().map( (item, idx) =>
        ` <option>${idx + 2}</option>`
        )}

        <option value="">- (approval)</option>
    </select>

    &nbsp;&nbsp;
    answers.

    &nbsp;&nbsp;
    &nbsp;&nbsp;
    Result Type:&nbsp;
    <select name="result_type">
        <option selected>absolute</option>
        <option>relative</option>
    </select>

    </p>

    <table id="answer_table" style="width:100%;">
      <tbody>
        <tr><th colspan="2">Question:</th><td><input type="text" name="question" size="70" /></td></tr>
        <tr><th>&nbsp;</th><th>&nbsp;</th><th>&nbsp;</th></tr>
      </tbody>
      <tfoot>
        <tr><th colspan="2"></th><th><a href="javascript:add_answers(document.getElementById('answer_table'), 5)">add 5 more answers</a></th></tr>
        <tr><td colspan="2"><input type="submit" value="add question" /></td></tr>
      </tfoot>

    </table>
  </form>
`
: `` }
`;