const BASE_TASKS_URL = `${location.origin}/api/tasks/`;
const sentTasks = document.getElementById('sent_tasks')


document.addEventListener("DOMContentLoaded", () => {
    fetchSentTasks()
});

async function fetchSentTasks() {
    const FETCH_SENT_TASK_URL = `${BASE_URL}?sent=${requestUserSlug}`;
  
    try {
      const response = await fetch(FETCH_SENT_TASK_URL);
      if (!response.ok) throw new Error('Failed to fetch sent tasks');
      const data = await response.json();
      displaySendTo(data)
    } catch (error) {
      console.error("Error fetching sent tasks:", error);
    }
}

function displaySendTo(tasks) {
    const taskCard = tasks.map(task => createSentTaskCard(task)).join('');
    sentTasks.innerHTML = taskCard

    tasks.forEach(task => {
      setEditSentTaskForm(task)
      setClientAcceptBtn(task)
    })
}

function createSentTaskCard(task) {
  
    return `
      <div class="col-xxl-4 col-xl-4 col-lg-4 col-md-6 col-sm-6"  id="sent-task-item-${task.id}">
        <div class="card task-item">
          <div class="card-body">
            <div class="d-flex align-items-center justify-content-between mt-5">
              <div class="lesson_name">
                <div class="d-flex align-items-center justify-content-center"> 
                    <h6 class="mb-0 fw-bold fs-6">${task.title}</h6>
                </div>
              </div>
              <div class="btn-group ms-2" role="group" aria-label="Basic outlined example">
                <button type="button" class="btn btn-outline-secondary" data-bs-toggle="modal" data-bs-target="#editsenttask-${task.id}">
                  <i class="icofont-edit text-success"></i>
                </button>
              </div>
            </div>
           <div class="row g-2 pt-4 mb-2">
              <div class="col-6">
                <div class="d-flex align-items-center">
                  <i class="icofont-check-alt"></i>
                  <span class="ms-2">Tamamlanma faizi:${task.completed_percent} %</span>
                </div>
              </div>
            </div> 
            <div class="card-footer">
              <button id="client-accept-${task.id}">${ !task.client_accepted ? 'Accept it' : 'Accepted' }</button>
            </div>
          </div>
        </div>
      </div>
    `;
}

async function sendTask(formData) {
    const url = `${BASE_TASKS_URL}send/`
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken
        },
        body: formData
      });
  
      if (!response.ok) throw new Error('Failed to send task');
  
    } catch (error) {
      console.log(error);
  
    }
}

async function editSentTask(formData, task) {
  const url = `${BASE_TASKS_URL}client/edit/${task.id}/`
  const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

  try {
    const response = await fetch(url, {
      method: 'PUT',
      headers: {
        'X-CSRFToken': csrfToken
      },
      body: formData
    });

    if (!response.ok) throw new Error('Failed to edit sent task');
    if (response.ok) {
      const data = await response.json();
      console.log(data);
      
      const previous_content = document.getElementById(`prevoiusContentTextarea-${task.id}`)
      previous_content.innerHTML = data.previous_content
    }

  } catch (error) {
    console.log(error);

  }
}

async function clientAccept(task) {
  const url = `${BASE_TASKS_URL}client/accept/${task.id}/`
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
      const taskCard = document.getElementById(`sent-task-item-${task.id}`);
      taskCard.outerHTML = createSentTaskCard(data);
    }
  } catch (error) {
      console.log(error);
  }
}

function setEditSentTaskForm(task) {
  const editSentTaskForm = document.getElementById(`editSentTaskForm-${task.id}`)
  editSentTaskForm.addEventListener('submit', function (e) {
    e.preventDefault()
    editSentTask((new FormData(editSentTaskForm)), task)
  })
}

function setClientAcceptBtn(task) {
  const clientAcceptBtn = document.getElementById(`client-accept-${task.id}`)
  clientAcceptBtn.addEventListener('click', function (e) {
    e.preventDefault()
    clientAccept(task)
  })
}