const h1 = document.querySelector('h1');
const href = window.location.href;
const href_ary = href.split('/');
const table = href_ary[href_ary.length - 2];

const uri = `http://127.0.0.1:3000/api/${table}/new`;
const name = document.querySelector('#name')
const email = document.querySelector('#email')

const element =
  table.charAt(0).toUpperCase() + table.slice(1, table.length - 1);
h1.innerHTML = element;


