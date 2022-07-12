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
        // update cart count
        Ui.updatecartcount()
    }
    static addtocart(product){
        const cart=document.querySelector('.cart')
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
    }
    // update cart count
    static updatecartcount(){
        cartcount=$('.cart-count')
        pdcts=Storage.get()
        cartcount.text(pdcts.length)
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




