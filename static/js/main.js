const form = document.querySelector('.axios-post');
// const date = form.elements.date;
// const price = form.elements.price;
// const quantity = form.elements.quantity;
// const provider = form.elements.providers;
// const collector = form.elements.collectors;
// const url = form.action;
// const submit = document.querySelector('#purchase-submit');

if (form) {

 console.dir(form);
  // form.addEventListener('submit', function (event) {
  //   event.preventDefault();
  //   const data = {
  //     date: date.value,
  //     price: price.value,
  //     quantity: quantity.value,
  //     id_provider: provider.value,
  //     id_collector: collector.value,
  //   };

  //   axios.post(url, data)
  //     .then(function (response) {
  //       console.log(response);
  //     })
  //     .catch(function (err) {
  //       console.log(err);
  //     });
  // });
} else {
  console.log('Not form present')
}
