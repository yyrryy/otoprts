class Product{
    constructor(id, name, price, img, stock){
        this.id=id
        this.name=name
        this.img=img
        this.price=price
        this.stock=stock
    }
}

class Ui{
    static displayprdcts(){
        const products=Storage.get()
        products.forEach(product=>{
            Ui.addtocart(product)
        })
        
    }
    static addtocart(product){
        const cart=document.querySelector('.cart')
        const cartbody=$('.cart-table__body')
        console.log(cartbody)
        cartbody.append(`
        <tr class="cart-table__row">
              <td class="cart-table__column cart-table__column--image">
                <div class="image image--type--product"><a href="product-full.html" class="image__body"><img class="image__tag" src="=${product.img}" alt=""></a></div>
              </td>
              <td class="cart-table__column cart-table__column--product"><a href="" class="cart-table__product-name">${product.name}</a>
                <ul class="cart-table__options">
                  <li>Color: Yellow</li>
                  <li>Material: Aluminium</li>
                </ul>
              </td>
              <td class="cart-table__column cart-table__column--price" data-title="Price">${product.price}</td>
              <td class="cart-table__column cart-table__column--quantity" data-title="Quantity">
                <div class="cart-table__quantity input-number">
                  <input class="form-control input-number__input" name="qty" data-price="${product.price}" type="number" min="1" value="1">
                  <div class="input-number__add"></div>
                  <div class="input-number__sub"></div>
                </div>
              </td>
              <td class="cart-table__column cart-table__column--total" data-title="Total">$<span class="total">${product.price}</span></td>
              <td class="cart-table__column cart-table__column--remove"><button type="button" class="cart-table__remove btn btn-sm btn-icon btn-muted"><svg width="12" height="12">
                    <path d="M10.8,10.8L10.8,10.8c-0.4,0.4-1,0.4-1.4,0L6,7.4l-3.4,3.4c-0.4,0.4-1,0.4-1.4,0l0,0c-0.4-0.4-0.4-1,0-1.4L4.6,6L1.2,2.6
            c-0.4-0.4-0.4-1,0-1.4l0,0c0.4-0.4,1-0.4,1.4,0L6,4.6l3.4-3.4c0.4-0.4,1-0.4,1.4,0l0,0c0.4,0.4,0.4,1,0,1.4L7.4,6l3.4,3.4
            C11.2,9.8,11.2,10.4,10.8,10.8z"></path>
                  </svg></button></td>
            </tr>
        `)
        const div=document.createElement('div')
        div.classList.add('product')
        div.innerHTML=`
        <div class="product-img">
            <img src="${product.img}" alt="">
        </div>
        <div class="product-info">
            <h4>${product.name}</h4>
            <p>$${product.price}</p>
            <p>In Stock: ${product.stock}</p>
        </div>
        `
        cart.appendChild(div)
        Ui.updatecartcount()
        Ui.updatetotal()
    }
    // update cart count
    static updatecartcount(){
        const cartcount=$('.cart-count')
        const pdcts=Storage.get()
        cartcount.text(pdcts.length)
    }
    // update total
    static updatetotal(){
        // get all inputs with name qty
        const qtys = $('input[name="qty"]')
  let bigtotal=$('.bigtotal')
  let tax=$('.tax')
  let shipping=$('.shipping')
  let subtotal = 0
  for (let i of qtys) {
    subtotal += parseFloat(i.dataset.price)
  }
  $('.subtotal').text(subtotal)
  bigtotal.text((parseFloat(subtotal)+parseFloat(shipping.text())+parseFloat(tax.text())).toFixed(2))
  for (let i of qtys){
    
    i.addEventListener('change', function(){
      let parent = i.parentElement.parentElement.parentElement
      let price = parseFloat(this.dataset.price)
      let total = parent.querySelector('.cart-table__column--total').querySelector('.total')
      let qty = parseFloat(i.value)
      // update total text
      let newTotal = (price * qty).toFixed(2)
      total.innerText = newTotal
      // total.contentText(price * qty)
      let subtotal = 0
      for (let i of $('.total')) {
        subtotal += parseFloat($(i).text())
      }
      
      $('.subtotal').text((subtotal).toFixed(2))
      bigtotal.text((parseFloat(subtotal) + parseFloat(shipping.text()) + parseFloat(tax.text())).toFixed(2))
    })
  }
    }
}

class Storage{
    static get(){
        let products=[]
        if(localStorage.getItem('products')===null){
            return products
        }
        products=JSON.parse(localStorage.getItem('products'))
        return products
    }
    static add(product){
        const products=Storage.get()
        products.push(product)
        localStorage.setItem('products', JSON.stringify(products))
    }
    
}




