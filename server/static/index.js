const h1 = document.querySelector('h1');
const btn_new = document.querySelector('#new')
const href = window.location.href;
const href_ary = href.split('/');
const table = href_ary[href_ary.length - 1];
const uri = `http://127.0.0.1:3000/api/${table}`;


h1.innerHTML = table.charAt(0).toUpperCase() + table.slice(1)
btn_new.href = `http://localhost:5000/js/${table}/new`
btn_new.innerHTML = `New ${table.slice(0, table.length - 1)}`


// async function getData(uri) {
//   const response = await fetch(uri);
//   const data = await response.json();
//   console.log(data.data);
//   return data.data;
// }

// getData(uri).then((data) => {
//   if (data) {
//     const fields = Object.keys(data[0]);
//     makeTableHead(fields);
//     makeTableBody(data);
//   }
// })

async function getData(uri) {
  try {
    const response = await axios.get(uri);
    const rows = response.data.data;
    const fields = Object.keys(rows[0]);
    makeTableHead(fields);
    makeTableBody(rows);
  } catch (er) {
    console.log(er);
  }
}


function makeTableHead(fields) {
  const thead = document.querySelector('#table-d-head');
  for (let field of fields) {
    const th = document.createElement('th');
    th.scope = 'col';
    th.innerHTML = field;
    thead.append(th);
  }
}

function makeTableBody(rows) {
  const tbody = document.querySelector('#table-d-body');
  rows.forEach((row) => {
    const items = Object.values(row);
    const href = `http://localhost:5000/js/${table}/${items[0]}`;
    const tr = document.createElement('tr');
    items.forEach((item) => {
      const td = document.createElement('td');
      const a = document.createElement('a');
      a.href = href;
      a.innerHTML = item;
      td.append(a);
      tr.append(td);
    });
    tbody.append(tr);
  });
}

getData(uri);