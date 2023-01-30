const input = document.querySelector('.input-btn input');
const listNotes = document.querySelector('.list-notes ul');
const message = document.querySelector('.list-notes');
let notes = [];

eventListeners();
function eventListeners(){
    document.addEventListener('DOMContentLoaded', () => {
        notes = JSON.parse(localStorage.getItem('notes')) || [];
        createHTML();
    });

    listNotes.addEventListener('click', deleteNote);
}

function deleteNote(e){
    if (e.target.tagName == 'SPAN') {
        const deleteId = parseInt(e.target.getAttribute('note-id'));
        notes = notes.filter(note => note.id !== deleteId);
        createHTML();
    }
}

function deleteAll(){
    notes = [];
    createHTML();
}

function addNotes(){
    const note = input.value;
    if (note === '') {
        alert('The field is empty...');
        return;
    }

    const noteObj = {
        note,
        id: Date.now()
    }
    notes = [...notes, noteObj]

    createHTML();
    input.value = '';
}

function createHTML(){
    clearHTML();

    if (notes.length > 0) {
        notes.forEach(note => {
            const li = document.createElement('li');
            li.innerHTML = `${note.note} <span note-id="${note.id}" >X</span>`;

            listNotes.appendChild(li);
        });
    }

    localStorage.setItem('notes', JSON.stringify(notes));
}


function clearHTML(){
    listNotes.innerHTML = '';
}