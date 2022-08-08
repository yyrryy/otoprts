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
        
        Ui.addtocart(products)
        
        
    }
  static addtocart(products){
        const cartbody=$('.cart-table__body')
        let trs=''
        for (let i of products){
          trs+=`
          <tr class="cart-table__row" data-id=${i.id}>
              <td class="cart-table__column cart-table__column--image">
                <div class="image image--type--product"><a href="product-full.html" class="image__body"><img class="image__tag" src="${i.img}" alt=""></a></div>
              </td>
              <td class="cart-table__column cart-table__column--product"><a href="" class="cart-table__product-name">${i.name}</a>
                <ul class="cart-table__options">
                  <li>Color: Yellow</li>
                  <li>Material: Aluminium</li>
                </ul>
              </td>
              <td class="cart-table__column cart-table__column--price" data-title="Price">${i.price}</td>
              <td class="cart-table__column cart-table__column--quantity" data-title="Quantity">
                <div class="cart-table__quantity input-number">
                  <input class="form-control input-number__input" name="qty" data-price="${i.price}" type="number" min="1" value="1">
                  <div class="input-number__add"></div>
                  <div class="input-number__sub"></div>
                </div>
              </td>
              <td class="cart-table__column cart-table__column--total" data-title="Total">$<span class="total">${i.price}</span></td>
              <td class="cart-table__column cart-table__column--remove"><button type="button" class="cart-table__remove btn btn-sm btn-icon btn-muted bi bi-x"></button></td>
            </tr>
          `
        }
        console.log(trs)
        cartbody.html(trs)
        // const div=document.createElement('div')
        // div.classList.add('product')
        // div.innerHTML=`
        // <div class="product-img">
        //     <img src="${product.img}" alt="">
        // </div>
        // <div class="product-info">
        //     <h4>${product.name}</h4>
        //     <p>$${product.price}</p>
        //     <p>In Stock: ${product.stock}</p>
        // </div>
        // `
        // cart.appendChild(div)
        Ui.updatecartcount()
        Ui.updatetotal()
        $('.input-number').customNumber();
    }
    // update cart count
    static updatecartcount(){
        const cartcount=$('.cart-count')
        const pdcts=Storage.get()
        cartcount.text(pdcts.length)
    }
    // upadate total in cart
    static updatecarttotal(t){
      let totalincart=$('.totalincart')
      totalincart.text(t)
    }  
    // update total
    static updatetotal(){
      console.log('updating total')
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
          console.log('changing')
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
          let bt=(parseFloat(subtotal) + parseFloat(shipping.text()) + parseFloat(tax.text())).toFixed(2)
          bigtotal.text(bt)
          Ui.updatecarttotal(bt)
        })
      }
      let t=parseFloat($('.bigtotal').text())
      Ui.updatecarttotal(t)
    }
    // remove product from cart
    static removeproduct(e){
        if(e.target.classList.contains('cart-table__remove')){
          let parent=e.target.parentElement.parentElement
          parent.remove()
          Ui.updatecartcount()
          Ui.updatetotal()
          Storage.remove(parent.dataset.id)
          Ui.displayprdcts()
          Ui.updatecartcount()
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
        var r = products.some((element, index) => {
          return element.id == product.id;
        });
        if (r) {
          alert('Product already in cart')
          return}
        products.push(product)
        localStorage.setItem('products', JSON.stringify(products))
        console.log('displaying products')
        Ui.displayprdcts()
        console.log('added')
        Ui.updatecartcount()
        console.log('updated')
        Ui.updatetotal()
        console.log('total updated')

    }
    // remove product from cart
    static remove(id){
      const products=Storage.get()
      products.forEach((product, index)=>{
          if(product.id===id){
              products.splice(index, 1)
          }
      })
      localStorage.setItem('products', JSON.stringify(products))
    }
}




