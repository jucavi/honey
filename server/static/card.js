const h1 = document.querySelector('h1');
const href = window.location.href;
const href_ary = href.split('/');
const table = href_ary[href_ary.length - 2];
const id = href_ary[href_ary.length - 1];

const uri = `http://127.0.0.1:3000/api/${table}/${id}`;

const element =
  table.charAt(0).toUpperCase() + table.slice(1, table.length - 1);
h1.innerHTML = element;

const img = document.querySelector('#card-img');
img.src = `${table.slice(0, table.length - 1)}.jpg`;

const btn_delete = document.querySelector('#delete');
btn_delete.addEventListener('click', (event) => {
  fetch(uri, { 'method': 'DELETE' })
    .then(res => {
      window.location.href = `http://localhost:5000/js/${table}`;
    })
    .catch(err => console.log(err))
});
