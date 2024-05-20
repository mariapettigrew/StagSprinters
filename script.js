$(document).ready(function() {
  
  $("#signInBtn").on("click", function() {
      let emailInput = $("#email-address").val();
      let passwordInput = $("#password").val();
      $.ajax({
          url: '/login',
          method: 'POST',
          data: {email: emailInput, password: passwordInput},
          success: function(response) {
              if (response.success) {
                  location.assign("/dashboard");
              } else {
                  alert("Login failed: " + response.message);
              }
          },
          error: function() {
              alert("An error occurred during login.");
          }
      });
  });


  $(".cartBtn").on("click", function() {
      location.assign("/cart")
  });


$("#checkoutBtn").on("click", function() {
    localStorage.setItem("totalPrice", $("#foodTotal").text());
    location.assign("/checkout")
    
    $.ajax({
        url: '/checkout',
        method: 'GET',
        data: {totalPrice: localStorage.getItem("totalPrice")},
        success: function(response) {
            console.log("I sent a POST") //debug statements
            console.log(response); 
        },
        error: function(xhr, status, error) {
            console.log("I sent a POST") //debug statements
            console.error(error); 
        }
    });
});


  
  $(".addBtn").on("click", function() {
      $(this).html(`✔`);
      setTimeout(() => {
          $(this).html("Add");
      }, 2000);
      let foodItem = $(this).siblings("h4").html();
      let foodPrice = $(this).siblings("p").attr("id");
      let foodImage = $(this).siblings("img").attr("src");
      $.ajax({
          url: '/add_to_cart',
          method: 'POST',
          contentType: 'application/json',
          data: JSON.stringify({
              foodItem: foodItem,
              foodPrice: foodPrice,
              foodImage: foodImage
          }),
          success: function(response) {
            alert("Item added to cart successfully!");
            updateCartDisplay(); 
          },
          error: function() {
              alert("An error occurred. Please try again.");
          }
      });
  });

  updateCartDisplay();  
});

function updateCartDisplay() {
  $.ajax({
      url: '/get_cart',
      method: 'GET',
      success: function(data) {
          $('#cartItems').empty();
          if (data.length === 0) {
              $('#cartItems').html(`<div class="h-[70vh] relative">
                                        <h3 class="absolute top-[100px] text-gray-400 text-6xl text-center font-proxima-nova w-2/3 mx-[15%]">Your Cart Is Currently Empty</h3>
                                    </div>`);
          } else {
              let totalPrice = 0;
              data.forEach(function(item, i) {
                  let itemPrice = parseFloat(item.foodPrice);
                  totalPrice += isNaN(itemPrice) ? 0 : itemPrice;
                  let itemHtml = `<div class="relative flex border-b-2 border-info-grey p-5">
                                      <img src="${item.foodImage}" alt="${item.foodItem}" class="w-[100px] h-[100px] mr-3">
                                      <div>
                                          <h4 class="text-[30px] ml-5 mt-3 font-Bree text-header-grey">${item.foodItem}</h4>
                                          <p class="text-[20px] font-Roboto">$${item.foodPrice}</p>
                                      </div>
                                      <button class="deleteBtn material-symbols-outlined absolute right-[10%] top-[65px] border-[2px] border-black h-[40px] w-[40px] rounded-full">delete</button>
                                  </div>`;
                  $('#cartItems').append(itemHtml);
              });
              $('#foodTotal').html(`Total: $${totalPrice.toFixed(2)}`);
          }
      },
      error: function() {
          alert('Failed to fetch cart items.');
      }
  });
}

$(document).on('click', '.deleteBtn', function() {
  var item = $(this).closest('.flex').find('h4').text();
  $.ajax({
      url: '/delete_from_cart',
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({ 'item': item }),
      success: function(response) {
          console.log(response.message);
          updateCartDisplay();
          $('#foodTotal').html(`Total: $${response.totalPrice.toFixed(2)}`); 
      },
      error: function(xhr, status, error) {
          console.error(error);
      }
  });
});


