const BASE_URL = `${location.origin}/api/subtasks/`;
const subtasks_container = document.getElementById('subtasks')
const createSubtaskForm = document.getElementById('createSubtaskForm');
const cancelSubtaskCreate = document.getElementById('cancel-subtask-create')


document.addEventListener("DOMContentLoaded", () => {
    fetchSubtasks();
});
  
async function fetchSubtasks() {
    const FETCH_URL = `${BASE_URL}?task=${task}`;
  
    try {
      const response = await fetch(FETCH_URL);
      if (!response.ok) throw new Error('Failed to fetch subtasks');
      const data = await response.json();
      displaySubtasks(data);
    } catch (error) {
      console.error("Error fetching subtasks:", error);
    }
}
  
function displaySubtasks(subtasks) {
    const subtaskCards = subtasks.map(subtask => createSubtaskCard(subtask)).join('');
    subtasks_container.innerHTML = subtaskCards;
  
    subtasks.forEach(subtask => {
      setDeleteSubtaskBtn(subtask);
      setSubtaskEditForm(subtask)
      setSubtaskCompletedBtn(subtask)
    //   if (workspace.workspace_members.length > 0) {
    //     workspace.workspace_members.forEach(member => {
    //       setRemoveWorkspaceMemberBtn(workspace, member)
    //       setWorkspaceMemberRoleChangeForm(workspace, member)
    //     })
    //   }
  
    });
}
  
function createSubtaskCard(subtask) {
  
    return `
      <div class="col-xxl-4 col-xl-4 col-lg-4 col-md-6 col-sm-6"  id="subtask-item-${subtask.id}">
        <div class="card task-item">
          <div class="card-body">
            <div class="d-flex align-items-center justify-content-between mt-5">
              <div class="lesson_name">
                <div class="d-flex align-items-center justify-content-center"> 
                    <h6 class="mb-0 fw-bold fs-6">${subtask.job}</h6>
                </div>
              </div>
              <div class="btn-group ms-2" role="group" aria-label="Basic outlined example">
                <button type="button" class="btn btn-outline-secondary" data-bs-toggle="modal" data-bs-target="#editsubtask-${subtask.id}">
                  <i class="icofont-edit text-success"></i>
                </button>
                <button type="button" class="btn btn-outline-secondary" data-bs-toggle="modal" data-bs-target="#deletesubtask-${subtask.id}">
                  <i class="icofont-ui-delete text-danger"></i>
                </button>
                <button type="button" class="btn btn-outline-secondary" data-bs-toggle="modal" id="completesubtask-${subtask.id}">
                ${subtask.completed ? '<i class="icofont-check-circled"></i>' : '<i class="icofont-close-line-circled"></i>'}
                </button>
              </div>
            </div>
           <div class="row g-2 pt-4 mb-2">
              <div class="col-6">
                <div class="d-flex align-items-center">
                  <i class="icofont-paper-clip"></i>
                  <span class="ms-2">comments count</span>
                </div>
              </div>
              <div class="col-6">
                <div class="d-flex align-items-center">
                  <i class="icofont-group-students"></i>
                  ${
                    subtask.assigned_to ? 
                    `<span class="ms-2">${subtask.assigned_user.user.email}</span>` : 
                    '<span class="ms-2">no assigned</span>'
                  }
                </div>
              </div>
              <div class="col-6">
                    <div class="d-flex align-items-center">
                    <i class="icofont-clock-time"></i>
                    ${subtask.started_date}
                    </div>
              </div>
                <div class="col-6">
                    <div class="d-flex align-items-center">
                    <i class="icofont-clock-time"></i>
                    ${subtask.deadline}
                    </div>
              </div>
            </div> 
          </div>
        </div>
      </div>
    `;
}

async function createSubtask(formData) {
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    console.log(formData);
    
    try {
      const response = await fetch(BASE_URL, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken
        },
        body: formData
      });
  
      if (response.ok) {
        const data = await response.json();
        subtasks_container.innerHTML = createSubtaskCard(data) + subtasks_container.innerHTML;
        createSubtaskForm.reset();
      }
  
    } catch (error) {
        console.log(error);
        
    }
}

async function deleteSubtask(subtask) {
    const url = `${BASE_URL}${subtask.id}/`;
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  
    try {
      const response = await fetch(url, {
        method: 'DELETE',
        headers: {
          'X-CSRFToken': csrfToken,
          'Content-Type': 'application/json'
        }
      });
  
      fetchSubtasks();
    } catch (error) {
      console.log("Error deleting subtask:", error);
    }
}

async function editSubtask(formData, subtask) {
    const url = `${BASE_URL}${subtask.id}/`
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    
    try {
      const response = await fetch(url, {
        method: 'PUT',
        headers: {
          'X-CSRFToken': csrfToken
        },
        body: formData
      });

      console.log(response.text);
      
  
      if (response.ok) {
        const data = await response.json();
        const subtaskCard = document.getElementById(`subtask-item-${subtask.id}`);
        subtaskCard.outerHTML = createSubtaskCard(data);
      }
  
    } catch (error) {
        console.log(error);
    }
}

async function completeSubtask(subtask) {
  const url = `${BASE_URL}completed/${subtask.id}/`
  const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

  try {
    const response = await fetch(url, {
      method: 'PATCH',
      headers: {
        'X-CSRFToken': csrfToken,
        'Content-Type': 'application/json'
      },
    });

    if (response.ok) {
      const data = await response.json();
      const subtaskCard = document.getElementById(`subtask-item-${subtask.id}`);
      subtaskCard.outerHTML = createSubtaskCard(data);
    }
    fetchSubtasks()
  } catch (error) {
      console.log(error);
  }
}

createSubtaskForm.addEventListener('submit', function (e) {
    e.preventDefault();
    createSubtask(new FormData(createSubtaskForm));
});
  
cancelSubtaskCreate.addEventListener('click', function(e) {
    e.preventDefault()
    createSubtaskForm.reset()
})

function setSubtaskEditForm(subtask) {
    
    const ediSubtaskForm = document.getElementById(`editSubtaskForm-${subtask.id}`)
    ediSubtaskForm.addEventListener('submit', function (e) {
      e.preventDefault()
      editSubtask((new FormData(ediSubtaskForm)), subtask)
    })
    if (ediSubtaskForm) {
      setCancelSubtaskEditBtn(subtask, ediSubtaskForm)
      ediSubtaskForm.reset()
    }
}

function setDeleteSubtaskBtn(subtask) {
    const deleteSubtaskBtn = document.getElementById(`deletesubtask-${subtask.id}`)
    deleteSubtaskBtn.addEventListener('submit', function (e) {
      e.preventDefault()
      deleteSubtask(subtask)
    })
}

function setCancelSubtaskEditBtn(subtask, ediSubtaskForm) {
    const cancelEditSubtaskBtn = document.getElementById(`cancel-subtask-edit-${subtask.id}`)
    cancelEditSubtaskBtn.addEventListener('click', function (e) {
      e.preventDefault()
      ediSubtaskForm.reset()
    })
}

function setSubtaskCompletedBtn(subtask) {
  const completedSubtaskBtn = document.getElementById(`completesubtask-${subtask.id}`)
  completedSubtaskBtn.addEventListener('click', function (e) {
    e.preventDefault()
    completeSubtask(subtask)
  })
}