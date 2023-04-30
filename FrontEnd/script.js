baseURL = 'http://127.0.0.1:8000/tarefas'

const form = document.querySelector('form');
const tasksList = document.querySelector('#tasks');

// Event listener para o formulário de adicionar tarefas
form.addEventListener('submit', (event) => {
	event.preventDefault(); // Prevenir a atualização da página
	const description = form.elements.description.value;
	const responsible = form.elements.responsible.value;
	const level = form.elements.level.value;
	const priority = form.elements.priority.value;

	// Enviar solicitação POST para a API
	fetch('/tasks', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			description: description,
			responsible: responsible,
			level: level,
			priority: priority
		})
	})
	.then(response => response.json())
	.then(data => {
		// Adicionar a nova tarefa à lista de tarefas
		const taskElement = document.createElement('div');
		taskElement.innerHTML = `
			<h3>${data.description}</h3>
			<p><strong>Responsible:</strong> ${data.responsible}</p>
			<p><strong>Level:</strong> ${data.level}</p>
			<p><strong>Priority:</strong> ${data.priority}</p>
			<p><strong>Situation`
		})
})


