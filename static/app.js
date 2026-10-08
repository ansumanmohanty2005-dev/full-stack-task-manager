const form=document.querySelector("#taskForm"), list=document.querySelector("#taskList"), filter=document.querySelector("#filter");

async function loadTasks(){
  const res=await fetch(`/api/tasks?status=${filter.value}`);
  const tasks=await res.json();
  list.innerHTML="";
  if(!tasks.length){list.innerHTML='<div class="empty">No tasks found.</div>';return;}
  tasks.forEach(task=>{
    const card=document.createElement("article");
    card.className="task";
    card.innerHTML=`
      <h3>${escapeHtml(task.title)}</h3>
      <p>${escapeHtml(task.description||"No description.")}</p>
      <div class="meta">
        <span class="badge">Priority: ${task.priority}</span>
        <span class="badge">Status: ${task.status}</span>
      </div>
      <div class="actions">
        <button onclick="toggleTask(${task.id},'${task.status}')">${task.status==="Completed"?"Mark Pending":"Complete"}</button>
        <button class="danger" onclick="deleteTask(${task.id})">Delete</button>
      </div>`;
    list.appendChild(card);
  });
}
form.addEventListener("submit",async e=>{
  e.preventDefault();
  const payload={title:title.value,description:description.value,priority:priority.value};
  const res=await fetch("/api/tasks",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});
  if(res.ok){form.reset();priority.value="Medium";loadTasks();}
});
async function toggleTask(id,current){
  await fetch(`/api/tasks/${id}`,{method:"PUT",headers:{"Content-Type":"application/json"},body:JSON.stringify({status:current==="Completed"?"Pending":"Completed"})});
  loadTasks();
}
async function deleteTask(id){
  if(!confirm("Delete this task?"))return;
  await fetch(`/api/tasks/${id}`,{method:"DELETE"});loadTasks();
}
function escapeHtml(value){return String(value).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[c]));}
filter.addEventListener("change",loadTasks);loadTasks();
