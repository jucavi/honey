const form = document.querySelector('.axios-post');

function params() {
  const data = {};

  for (let element of form.elements) {
    const nodeName = element.nodeName.toLowerCase();
    if (nodeName === 'input' || nodeName === 'select') {
      data[element.name] = element.value;
    }
  }
  return data;
}

function reset_default() {
  const data = {};

  for (let element of form.elements) {
    const nodeName = element.nodeName.toLowerCase();

    if (nodeName === 'input') {
      element.value = '';
    }

    if (nodeName === 'select') {
      for (let option of element.options) {
        if (option.defaultSelected) {
          option.selected = true;
          break;
        }
      }
    }
  }
  return data;
}

if (form) {
  const url = form.action;

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    axios
      .post(url, params())
      .then(function (response) {
        reset_default();
        console.log(response);
      })
      .catch(function (err) {
        console.log(err);
      });
  });
}
