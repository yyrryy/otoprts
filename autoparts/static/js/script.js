// declare
const byref = $(".byref");
const bychas = $(".bychas");

const ref = $(".ref"); 
const chas = $(".chas");
const catg = $(".catg");

ref.val('')
chas.val('')
catg.val(0)

const searchref = $(".searchref");
const searchchas = $(".searchchas");

searchchas.attr("disabled", true);
searchref.attr("disabled", true);

bychas.on("input", () => {
  chas.val().length > 3 && catg.val() != 0
    ? searchchas.attr("disabled", false)
    : searchchas.attr("disabled", true);
});


byref.on("input", () => {
  ref.val().length > 3
    ? searchref.attr("disabled", false)
    : searchref.attr("disabled", true);
});

byref.on('submit', (e) => {
  searchref.addClass("btn-loading").text("");
  e.preventDefault();
  const nref=ref.val();
  $.ajax({
    type: "POST",
    url: "/byref",
    data: {
      ref: nref,
      csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
    },
    success: (data) => {
      searchref.removeClass("btn-loading").text("Search");
      $(".pdctsholder").html('')
      if (data.valid) {
        $("html,body").animate(
          {
            scrollTop: $(".selectproducts").offset().top,
          },
          "slow"
        );
        $(".pdctsholder").html(`
        <div class="products-list__item">
                          <div class="product-card">
                        
                            <div class="product-card__image">
                              <div class="image image--type--product"><div class="image__body"><img class="image__tag"
                                    src="${data.img}" alt="${data.name}"></div></div>
                              <div
                                class="status-badge status-badge--style--success product-card__fit status-badge--has-icon status-badge--has-text">
                                <div class="status-badge__body">
                                  <div class="status-badge__icon"><svg width="13" height="13">
                                      <path d="M12,4.4L5.5,11L1,6.5l1.4-1.4l3.1,3.1L10.6,3L12,4.4z">
                                      </path>
                                    </svg></div>
                                  <div class="status-badge__text">Part Fit for 2011 Ford Focus S</div>
                                  <div class="status-badge__tooltip" tabindex="0" data-toggle="tooltip" title=""
                                    data-original-title="Part Fit for 2011 Ford Focus S"></div>
                                </div>
                              </div>
                            </div>
                            <div class="product-card__info">
                            <div class='product-card__meta d-flex justify-content-between'>
                              
                              <div>
                                <span class="product-card__meta-title">REF:</span>${data.ref}
                              </div>
                              <div>
                                <span class="product-card__meta-title">REF:</span><img class="border image__tag" src='https://countryflagsapi.com/png/${data.country}' width=30 height=20/>
                              </div>
                            </div>
                              <div class="product-card__name">
                                <div>
                                  <div class="product-card__badges">
                        
                                  </div>${data.name}
                                </div>
                              </div>
                        
                        
                            </div>
                            <div class="product-card__footer">
                              <div class="product-card__prices">
                                <div class="product-card__price product-card__price--current">${data.price} DH <br> <small>${data.stock} unities in stock</small></div>
                              </div><button class="product-card__addtocart-icon" type="button" aria-label="Add to cart"><svg width="20"
                                  height="20">
                                  <circle cx="7" cy="17" r="2"></circle>
                                  <circle cx="15" cy="17" r="2"></circle>
                                  <path
                                    d="M20,4.4V5l-1.8,6.3c-0.1,0.4-0.5,0.7-1,0.7H6.7c-0.4,0-0.8-0.3-1-0.7L3.3,3.9C3.1,3.3,2.6,3,2.1,3H0.4C0.2,3,0,2.8,0,2.6
                                                	V1.4C0,1.2,0.2,1,0.4,1h2.5c1,0,1.8,0.6,2.1,1.6L5.1,3l2.3,6.8c0,0.1,0.2,0.2,0.3,0.2h8.6c0.1,0,0.3-0.1,0.3-0.2l1.3-4.4
                                                	C17.9,5.2,17.7,5,17.5,5H9.4C9.2,5,9,4.8,9,4.6V3.4C9,3.2,9.2,3,9.4,3h9.2C19.4,3,20,3.6,20,4.4z">
                                  </path>
                                </svg></button>
                              <button class="product-card__addtocart-full" type="button">Add
                                to cart</button>
                            </div>
                          </div>
                        </div>
        `);
      }
      else {
        console.log('here')
        searchref.removeClass("btn-loading").text("Search");
        alert("N° ref " + nref + " Nt founf");
        
      }
    },
    error: (err) => {
      console.log(err)
      searchref.removeClass("btn-loading").text("Search");

    },
  });
})

bychas.on('submit', (e) => {
  searchchas.addClass('btn-loading').text('')
  e.preventDefault();
  const nchas=chas.val()
  $.ajax({
    type: "POST",
    url: "/bychas",
    data: {
      chas: nchas,
      catg:catg.val(),
      csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
    },
    success: (data) => {
      searchchas.removeClass("btn-loading").text("Search");
      $(".pdctsholder").html('')
      if (data.valid) {
        $("html,body").animate(
          {
            scrollTop: $(".selectproducts").offset().top,
          },
          "slow"
        );
        data.pdcts.map((e) => {
          $(".pdctsholder").append(`
        <div class="products-list__item">
                          <div class="product-card">
                        
                            <div class="product-card__image">
                              <div class="image image--type--product"><div class="image__body"><img class="image__tag"
                                    src="${e.img}" alt="${e.name}"></div></div>
                              <div
                                class="status-badge status-badge--style--success product-card__fit status-badge--has-icon status-badge--has-text">
                                <div class="status-badge__body">
                                  <div class="status-badge__icon"><svg width="13" height="13">
                                      <path d="M12,4.4L5.5,11L1,6.5l1.4-1.4l3.1,3.1L10.6,3L12,4.4z">
                                      </path>
                                    </svg></div>
                                  <div class="status-badge__text">Part Fit for 2011 Ford Focus S</div>
                                  <div class="status-badge__tooltip" tabindex="0" data-toggle="tooltip" title=""
                                    data-original-title="Part Fit for 2011 Ford Focus S"></div>
                                </div>
                              </div>
                            </div>
                            <div class="product-card__info">
                              <div class='product-card__meta d-flex justify-content-between'>
                              
                              <div>
                                <span class="product-card__meta-title">REF:</span>${e.ref}
                              </div>
                              <div>
                                <span class="product-card__meta-title">Factory:</span><img class="border image__tag" src='https://countryflagsapi.com/png/${e.country}' width=30 height=20/>
                              </div>
                            </div>
                              <div class="product-card__name">
                                <div>
                                  <div class="product-card__badges">
                        
                                  </div>${e.name}
                                </div>
                              </div>
                        
                        
                            </div>
                            <div class="product-card__footer">
                              <div class="product-card__prices">
                                <div class="product-card__price product-card__price--current">${e.price} DH<br> <small>${e.stock} unities in stock</small></div>
                              </div><button class="product-card__addtocart-icon" type="button" aria-label="Add to cart"><svg width="20"
                                  height="20">
                                  <circle cx="7" cy="17" r="2"></circle>
                                  <circle cx="15" cy="17" r="2"></circle>
                                  <path
                                    d="M20,4.4V5l-1.8,6.3c-0.1,0.4-0.5,0.7-1,0.7H6.7c-0.4,0-0.8-0.3-1-0.7L3.3,3.9C3.1,3.3,2.6,3,2.1,3H0.4C0.2,3,0,2.8,0,2.6
                                                	V1.4C0,1.2,0.2,1,0.4,1h2.5c1,0,1.8,0.6,2.1,1.6L5.1,3l2.3,6.8c0,0.1,0.2,0.2,0.3,0.2h8.6c0.1,0,0.3-0.1,0.3-0.2l1.3-4.4
                                                	C17.9,5.2,17.7,5,17.5,5H9.4C9.2,5,9,4.8,9,4.6V3.4C9,3.2,9.2,3,9.4,3h9.2C19.4,3,20,3.6,20,4.4z">
                                  </path>
                                </svg></button>
                              <button class="product-card__addtocart-full" type="button">Add
                                to cart</button>
                            </div>
                          </div>
                        </div>
        `);
        });
        searchchas.removeClass("btn-loading").text("Search");
      }
      else {
        console.log('zedze')
        searchchas.removeClass("btn-loading").text("Search");
        alert('N° chasis '+nchas+' Nt founf')
      }
    },
    error: (err) => {
      console.log(err);
      searchchas.removeClass("btn-loading").text("Search");

    },
  });
})