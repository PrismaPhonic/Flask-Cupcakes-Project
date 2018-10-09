const cupcakeSession = new CupcakeMethods();

$(document).ready(function () {
  // ON LOAD, GET LIST OF CUPCAKES
  $.get('/cupcakes', function (resp) {
    cupcakeSession.showAllCupcakes();
  })

  // EVENT HANDLERS
  // ADD CUPCAKE BUTTON HANDLER
  $('#add-cupcake-button').on('click', function (evt) {
    const flavor = $('#flavor').val();
    const rating = $('#rating').val();
    const size = $('#size').val();
    const url = $('#url').val() === '' ? undefined : $('#url').val();

    let data = { flavor, rating, size, url, }

    cupcakeSession.addCupcake(data, function (resp) {
      let cupcake = resp.response; referals
      cupcakeSession.appendCupcakeToDOM(cupcake);
    })
  })

  // SEARCH BUTTON HANDLER
  $('#search').on('input', function (evt) {
    const search = $('#search').val().toLowerCase();
    $.get('/cupcakes', { search, }, function (resp) {
      $('#cupcakes').empty();
      $('.jumbotron h1').text(search.replace(/^\w/, c => c.toUpperCase()) + ' Cupcakes')
      for (let cupcake of resp.response) {
        cupcakeSession.appendCupcakeToDOM(cupcake);
      }
    })
  })

  // REMOVE CUPCAKE X BUTTON
  $('#cupcakes').on('click', '.close', function (evt) {
    evt.preventDefault();
    let cupcakeId = $(this).attr('id');
    cupcakeSession.deleteCupcake(cupcakeId, (resp) => {
      cupcakeSession.showAllCupcakes();
    })
  })

  // EDIT CUPCAKE BUTTON
  $('#edit-cupcake-button').on('click', function (evt) {
    const flavor = $('#edit-flavor').val();
    const rating = $('#edit-rating').val();
    const size = $('#edit-size').val();
    const url = $('#edit-url').val() === '' ? undefined : $('#url').val();
    const id = +$("#edit-cupcake-button i").attr('id');

    let data = { id, flavor, rating, size, url, }
    console.log(data);

    cupcakeSession.editCupcake(data, function (resp) {
      let cupcake = resp.response;
      window.location.href = "/";
    })
  })
})