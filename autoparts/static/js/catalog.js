
const client = $('select[name="client"]');
const tablecmnd = $('.commande-table');
const csrf= $("[name=csrfmiddlewaretoken]").val()


// filter table function
function searchtable() {
    // Declare variables
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("myInput");
    // lower the input value
    filter = input.value.toLowerCase();
    table = document.getElementById("myTable");
    tr = table.getElementsByTagName("tr");
  
    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[1];
      if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.includes(filter)) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }
    }
}

const checkstorage = (id)=>{
    products=JSON.parse(localStorage.getItem('products')) || []
    if(products.includes(id)){
        return true
    }
    return false
}

const clearstorage =()=>{
    // clear localstorage
    localStorage.removeItem('products')
    localStorage.removeItem('productsdetails')
    // clear table
    tablecmnd.empty()
}

const savetostorage=(id, ref, n, qty, pr, tt)=>{
    // get products from localstorage
    products=JSON.parse(localStorage.getItem('products')) || []
    productsdetails=JSON.parse(localStorage.getItem('productsdetails')) || []
    // add the new product
    let pdct=[ref, n, qty, pr, tt]
    products.push(id)
    productsdetails.push(pdct)
    // save to localstorage
    localStorage.setItem('products', JSON.stringify(products))
    localStorage.setItem('productsdetails', JSON.stringify(productsdetails))
}

const updatetotal=()=>{
    t=0
    $('.subtotal').each((i, el)=>{
        t+=parseFloat($(el).text())
    })
    $('.total').text(t.toFixed(2))
}

const loadpdcts=()=>{
    products=JSON.parse(localStorage.getItem('productsdetails'))
    if (products && products.length){
        $('.valider').prop('disabled', false)
        for (i of products){
            let [ref, n, qty, pr, tt]=i
            tablecmnd.append(`
            <tr class="cmndholder">
            <td class="pdctcmnd" ref=${ref} name="${n}">
                ${ref}
            </td>
            <td class="pdctcmnd" ref=${ref} name="${n}">
                ${n}
            </td>
            <td class="qtyholder">
                <div class="cart-table__quantity input-number"><input class="form-control input-number__input qty" type="number" min="0" value="${qty}" price="${pr}" name='qtytosub'><div class="input-number__add"></div><div class="input-number__sub"></div></div>
                
            </td>
            <td class="subtotal">
                ${tt}
                
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

const loading=()=>{
    $('.loading').removeClass('d-none').addClass('d-flex');
}

const stoploading=()=>{
    $('.loading').removeClass('d-flex').addClass('d-none');
}

const addcmnd=(name, ref, qty, pr, id)=>{
    if(!checkstorage(id)){
        sub=(pr*qty).toFixed(2)
        savetostorage(id, ref, name, qty, pr, sub)
        $('.commanditems').text(parseInt($('.commanditems').text())+1)
        $('.valider').prop('disabled', false)
        tablecmnd.append(`
        <tr class="cmndholder">
        <td class="pdctcmnd" ref=${ref} name="${name}">
            ${ref}
        </td>
        <td class="pdctcmnd" ref=${ref} name="${name}">
            ${name}
        </td>
        <td class="qtyholder">
            <div class="cart-table__quantity input-number"><input class="form-control input-number__input qty" type="number" min="0" value="${qty}" price="${pr}" name='qtytosub'><div class="input-number__add"></div><div class="input-number__sub"></div></div>
            
        </td>
        <td class="subtotal">
            ${sub}
            
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
        return
    }
    alert('Deja commandée')

}


const validercmnd=(clientid)=>{
    holder=$('.cmndholder')
    commande=[]
    holder.each((i, el)=>{
        ref=$(el).find('.pdctcmnd').attr('ref')
        n=$(el).find('.pdctcmnd').attr('name')
        qty=$(el).find('.qtyholder .input-number > .qty').val()
        cmd=ref+':'+n+':'+qty
        commande.push(cmd)
    })
    $.ajax({
        url: '/commande',
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrf,
            'commande': commande,
            'client':clientid,
            'total':parseFloat($('.total').text())
        },

        success: function(data){
            $('.cmndholder').remove()
            $('.valider').prop('disabled', true)
        },
        error:(err)=>{
            alert(err)
        }
    })
}


const close = function() {

    $('body').css({
        'overflow': 'auto',
        'paddingRight': ''
    });
};
const open = function() {

    $('body').css({
        'overflow': 'hidden',
        'paddingRight': ''
    });
};

const updateclients=()=>{
    loading()
    $.ajax({
        url: '/clients',
        type: 'GET',
        
        success: function(data){
            stoploading()
            $('[name=client]').html('<option value="0">---</option>')
            for (i of JSON.parse(data.clients)){
                $('[name=client]').append(`
                <option value="${i.id}">${i.name} ${i.phone}</option>
                `)
            }
        },
        error:(err)=>{
            stoploading()
            alert(err)
        }
    })
}


$("#addclientform").submit(function(event) {
    event.preventDefault();

    var formData = $(this).serialize();
    console.log(formData)
    loading()
    $.ajax({
      type: "POST",
      url: "/addclient",
      data: formData,
      success: function(response) {
        stoploading()
        // handle the response from the server
        console.log(response)
        $('#addclientmodal').modal('hide')
        updateclients()
      }
    });
  });

// handle .addclient click
// const addclientform=(e)=>{
//     e.preventDefault()
//     $.ajax({
//         url: '/addclient',
//         type: 'POST',
//         data: {
//             nom: $('input[name="nom"]').val(),
//             city: $('input[name="city"]').val(),
//             phone: $('input[name="phone"]').val(),
//             csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
//         },
//         success: function(response){
//             console.log(response)
//             $('#addclientmodal').modal('hide')
//             updateclients()
//         }
//     })
// }

// clear commande
const clearcommande=()=>{
    clearstorage()
    $('.valider').prop('disabled', true)
    $('.total').text('0.00')
}


$(document).ready(function() {
    loading()
    stoploading()
    loadpdcts()
});


$('[name=category]').on('change',() => {
            loading()
    
            $.ajax({
                method:'Post',
                url:'/filters',
                data:{
                csrfmiddlewaretoken:csrf,
                category:$('select[name=category]').val()=='0'?null:+$('select[name=category]').val(),
                brand:$('input[name="brand"]').val()=='0'?null:$('input[name="brand"]').val(),
                model:$('input[name="model"]').val()=='0'?null:$('input[name="model"]').val(),
                mark:$('input[name="mark"]').val()=='0'?null:$('input[name="mark"]').val()
            },
                success:(data)=>{
                    stoploading()
                    $('.prdctslist').html(data.data)
                    $('.input-number').customNumber();
                    $('.cmnd').each((i, el)=>{
                        $(el).on('click', ()=>{
                            
                            // id=$(el).attr('pdct');
                            $(el).attr('disabled', true)
                            ref=$(el).attr('pdctref')
                            name=$(el).attr('pdctname')
                            pr=$(el).attr('pdctpr')
                            id=$(el).attr('pdctid')
                            // get nearest item
                            let qty = $(el).parent().find('.input-number > .input-number__input').val()
                            // add new row to coommand table
                            addcmnd(name, ref, qty, pr, id)
                            // update total
                            updatetotal()

                        })
                    })
                },
                Error:(error)=>{
                    stoploading()
                    alert('error')
                    console.log(error)
                }
    
            })
    
    
        })

$('.valider').on('click', ()=>{
    clientid=client.val()
    if(clientid=='0'){
        $('.clienterr').removeClass('d-none').addClass('d-block')
        return
    }
    else{
        $('.valider').prop('disabled', false)
        $('.clienterr').removeClass('d-block').addClass('d-none')
        validercmnd(clientid)
        clearstorage()
        // refresh window
        window.location.reload()


    }
})
