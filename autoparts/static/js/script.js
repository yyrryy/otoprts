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

document.addEventListener('DOMContentLoaded', Ui.displayprdcts)

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
  const nref=ref.val().toLowerCase();
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
                                <span class="product-card__meta-title">REF:</span><img class="border image__tag" src='https://countryflagsapi.com/png/${data.country}' alt="${data.country}" width=30 height=20/>
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
                              </div><button class="add-to-cart bi bi-cart-plus" 
                              data-id="${data.id}"
                              data-price="${data.price}"
                              data-name="${data.name}"
                              data-img="${data.img}"
                              data-stock="${data.stock}"
                              type="button" aria-label="Add to cart"></button>
                              
                            </div>
                          </div>
                        </div>
        `);
        console.log('by ref')
        bts_addtocats=$('.add-to-cart')
        bts_addtocats.each((i, el)=>{
            $(el).on('click', (e)=>{
                // disable this button
                $(el).attr('disabled', true)
                $(el).removeClass('bi-cart-plus').addClass('bi-cart-check')
                const id=e.target.dataset.id
                const name=e.target.dataset.name
                const price=e.target.dataset.price
                const img=e.target.dataset.img
                const stock=e.target.dataset.stock
                pdct=new Product(id, name, price, img, stock)
                console.log('saving')
                Storage.add(pdct)
                console.log("displaying")
                

            })
                
        })
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
  const nchas=chas.val().toLowerCase();
  // lowercase the string

  const fff=$("[name=csrfmiddlewaretoken]").val()
  $.ajax({
    type: "POST",
    url: "/bychas",
    data: {
      chas: nchas,
      catg:catg.val(),
      csrfmiddlewaretoken: fff
      
    },
    success: (data) => {
      if (data.valid) {
        $("html,body").animate(
            {
              scrollTop: $(".selectproducts").offset().top,
            },
            "slow"
          );
        $(".pdctsholder").html('')
        
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
                                <div class="product-card__price product-card__price--current">${e.price} DH <br> <small>${e.stock} unities in stock</small></div>
                              </div><button class="add-to-cart bi bi-cart-plus" 
                              data-id="${e.id}"
                              data-price="${e.price}"
                              data-name="${e.name}"
                              data-img="${e.img}"
                              data-stock="${e.stock}"
                              type="button" aria-label="Add to cart"></button>
                            </div>
                          </div>
                        </div>
        `);
        });
        console.log('by chas')
        bts_addtocats=$('.add-to-cart')
        console.log(bts_addtocats)
        // convert code above to jquery
        bts_addtocats.each((i, el)=>{
            $(el).on('click', (e)=>{
                // disable this button
                $(el).attr('disabled', true)
                $(el).removeClass('bi-cart-plus').addClass('bi-cart-check')
                const id=e.target.dataset.id
                const name=e.target.dataset.name
                const price=e.target.dataset.price
                const img=e.target.dataset.img
                const stock=e.target.dataset.stock
                pdct=new Product(id, name, price, img, stock)
                console.log('saving')
                Storage.add(pdct)

            })
          })
        // convert the coded above to jquery
        // $(".add-to-cart").on('click', (e)=>{
        //     // disable this button
        //     $(e.target).attr('disabled', true)
        //     $(e.target).removeClass('bi-cart-plus').addClass('bi-cart-check')
        //     const id=e.target.dataset.id
        //     const name=e.target.dataset.name
        //     const price=e.target.dataset.price
        //     const img=e.target.dataset.img
        //     const stock=e.target.dataset.stock
        //     pdct=new Product(id, name, price, img, stock)
        //     console.log('saving')
        //     Storage.add(pdct)
        // })

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


//get products from local storage
pdcts=Storage.get().length
// update cart count
$('.mobile-indicator__counter').text(pdcts)
$('.cart-table__body').on('click', (e) => {
  console.log(e.target)
  // remove product from ui
  Ui.removeproduct(e)
})



