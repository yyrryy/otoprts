$(document).ready(function () {
    
    const updatetotal=()=>{
        t=0
        $('.subtotal').each((i, el)=>{
            t+=parseFloat($(el).text())
        })
        $('.total').text(t.toFixed(2))
    }


    const clearstorage =()=>{
        // clear localstorage
        localStorage.removeItem('products')
        localStorage.removeItem('productsdetails')
        // clear table
        $('.cart-table__body').empty()
        //$('.prdctslist').empty()
        $('.commanditems').text(0)
        updatetotal()
    }

    const validercmnd=(clientid)=>{
        holder=$('.cmndholder')
        commande=[]
        holder.each((i, el)=>{
            ref=$(el).attr('ref')
            n=$(el).attr('n')
            qty=$(el).find('.qtyholder .input-number > .qty').val()
            cmd=ref+':'+n+':'+qty
            commande.push(cmd)
        })
        console.log(commande)
        $.ajax({
            url: '/commande',   
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
                'commande': commande,
                'client':clientid,
                'total':parseFloat($('.total').text()),
                'modpymnt':$('[name="modpymnt"]').val(),
                'modlvrsn':$('[name="modlvrsn"]').val()
            },
    
            success: function(data){
                $('select').val(0)
                $('.modes').removeClass('border-danger')
                stoploading()
                $('.cmndholder').remove()
                clearstorage()
                $('.valider').prop('disabled', true)
                        $('.fromclient').prop('disabled', true)
                alert('Commande envoyé')
                // go to thank you 
                window.location.href='/salsemanorders'
            },
            error:(err)=>{
                stoploading()
                alert(err)
            }
        })
    }

    // valider click
    $('.valider').on('click', ()=>{
        loading('verification')
        //
        if ($('[name="modpymnt"]').val()==0 || $('[name="modlvrsn"]').val()==0){
            stoploading()
            alert('Veuillez choisir un mode de payement ou de livraison')
            $('.modes').addClass('border-danger')
            return
        }
        clientid=$('.clientid').val()
        validercmnd(clientid)
    })

    
    
    $('.input-number').customNumber();
    $("input[name=qtytosub]").each((i, el)=>{
        $(el).on('change', ()=>{
            v=$(el).val()
            subt=$(el).attr('price')*v
            // find the subtotal cell
            $(el).parent().parent().parent().find('.subtotal').text(subt.toFixed(2))
            updatetotal()
        }
    )})
    //get items from local storage
    const loadpdcts=()=>{
        products=JSON.parse(localStorage.getItem('productsdetails'))
        $('.loadingcartitems').addClass('d-none')
        if (products && products.length){
            $('.valider').prop('disabled', false)
            $('.fromclient').prop('disabled', false)
            for (i of products){
                let [ref, n, ctg, qty, pr, tt, img, min, id]=i
                $('.cart-table__body').append(`
                <tr class="cart-table__row cmndholder" ref="${ref}" n=${n}">
                <td class="cart-table__column cart-table__column--product">
                  <small>${ref}</small>
                </td>
                <td class="cart-table__column cart-table__column--product">
                  <small>${ctg} ${n}</small>
                </td>
                <td class="cart-table__column cart-table__column--price" data-title="Price">
                <small>${pr}</small>
                </td>
                <td class="cart-table__column cart-table__column--quantity qtyholder" data-title="Quantity">
                  <div class="cart-table__quantity input-number">
                    <input readonly class="form-control input-number__input qty" type="number" min="${min?min:1}" value="${qty}" price=${pr} name="qtytosub">
                    <div class="input-number__add"></div>
                    <div class="input-number__sub"></div>
                  </div>
                </td>
                <td class="cart-table__column cart-table__column--total subtotal" data-title="Total">
                <small>${tt}</small>
                </td>
                <td class="cart-table__column cart-table__column--remove">
                  <button type="button" class="cart-table__remove btn btn-sm btn-icon btn-muted" id="${id}">
                    <svg width="12" height="12">
                      <path d="M10.8,10.8L10.8,10.8c-0.4,0.4-1,0.4-1.4,0L6,7.4l-3.4,3.4c-0.4,0.4-1,0.4-1.4,0l0,0c-0.4-0.4-0.4-1,0-1.4L4.6,6L1.2,2.6
      c-0.4-0.4-0.4-1,0-1.4l0,0c0.4-0.4,1-0.4,1.4,0L6,4.6l3.4-3.4c0.4-0.4,1-0.4,1.4,0l0,0c0.4,0.4,0.4,1,0,1.4L7.4,6l3.4,3.4
      C11.2,9.8,11.2,10.4,10.8,10.8z"></path>
                    </svg>
                  </button>
                </td>
              </tr>
                `)
                $('.input-number').customNumber();
                $("input[name=qtytosub]").each((i, el)=>{
                    $(el).on('change', ()=>{
                        v=$(el).val()
                        subt=$(el).attr('price')*v
                        // find the subtotal cell
                        $(el).parent().parent().parent().find('.subtotal').text(subt.toFixed(2))
                        updatetotal()
                    }
                )})
            }
            updatetotal()
            return
        }
    }
    loading()
    stoploading()
    loadpdcts()
    // cart delete item
    $('.cart-table__remove').click(function () {
      if (confirm("Supprimer l'article ?")){
        $(this).closest('tr').remove();
        updatetotal()
        // remove from local storage
        products=JSON.parse(localStorage.getItem('products'))
        id=$(this).attr('id')
        // using splice
        products.splice(products.indexOf(id), 1)
        localStorage.setItem('products', JSON.stringify(products))
        // remove from local storage
        productsdetails=JSON.parse(localStorage.getItem('productsdetails'))
        productsdetails.splice(productsdetails.indexOf(id), 1)
        localStorage.setItem('productsdetails', JSON.stringify(productsdetails))
        $('.commanditems').text(parseInt($('.commanditems').text())-1)
        // check if cart is empty
        if (products.length==0){
            $('.valider').prop('disabled', true)
        }


      }
    });
  });