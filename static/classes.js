class CupcakeMethods {
  constructor() {
    this.BASE_URL = 'http://127.0.0.1:5000';
  };

  showAllCupcakes() {
    $('#cupcakes').empty();
    $.get('/cupcakes', (resp) => {
      for (let cupcake of resp.response) {
        this.appendCupcakeToDOM(cupcake);
      }
    })
  };

  addCupcake(data, cb) {
    $.ajax({
      method: "POST",
      url: `${this.BASE_URL}/cupcakes`,
      contentType: "application/json",
      data: JSON.stringify(data),
      success: (resp) => {
        cb(resp);
      }
    })
  };

  editCupcake(cupcake, cb) {
    $.ajax({
      method: "PATCH",
      url: `${this.BASE_URL}/cupcakes/${cupcake.id}`,
      contentType: "application/json",
      data: JSON.stringify(cupcake),
      success: (resp) => {
        cb(resp);
      }
    })
  };

  deleteCupcake(id, cb) {
    $.ajax({
      method: "DELETE",
      url: `${this.BASE_URL}/cupcakes/${id}`,
      success: (resp) => {
        cb(resp);
      }
    })
  };

  appendCupcakeToDOM(cupcake) {
    let cupcake_html = `
    <div class="col-4">
      <a href="/cupcakes/${cupcake.id}">
        <div class="card text-white bg-primary mb-3">
          <div class="card-header">${cupcake.flavor}
          <button type="button" class="close" id="${cupcake.id}" data-dismiss="card">&times;</button>
          </div>
          <div class="card-body">
            <p class="card-text">${cupcake.size} ${cupcake.flavor} cupcake that has a rating of ${cupcake.rating}</p>
            <img src="${cupcake.image}" class="img-thumbnail"></img>
            </div>
        </div>
      </a>
    </div>
    `;
    $('#cupcakes').append($(cupcake_html));
  };
}