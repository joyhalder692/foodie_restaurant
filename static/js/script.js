// ==========================================
// FOOD SEARCH
// ==========================================

function searchFood() {

    const searchInput =
        document.getElementById("searchInput");

    if (!searchInput) {
        return;
    }

    const searchText =
        searchInput.value
            .toLowerCase()
            .trim();

    const cards =
        document.querySelectorAll(".menu-card");

    let found = false;


    cards.forEach(function(card) {

        const nameElement =
            card.querySelector("h3");

        const descriptionElement =
            card.querySelector("p");

        const name =
            nameElement
                ? nameElement.innerText.toLowerCase()
                : "";

        const description =
            descriptionElement
                ? descriptionElement.innerText.toLowerCase()
                : "";

        const category =
            card.getAttribute("data-category")
                ? card.getAttribute("data-category").toLowerCase()
                : "";


        if (
            name.includes(searchText) ||
            category.includes(searchText) ||
            description.includes(searchText)
        ) {

            card.style.display = "";

            found = true;

        } else {

            card.style.display = "none";

        }

    });


    let noResult =
        document.getElementById("no-food-result");


    if (!found && searchText !== "") {

        if (!noResult) {

            noResult =
                document.createElement("div");

            noResult.id =
                "no-food-result";

            noResult.innerHTML =
                "😔 No food found.";

            noResult.style.textAlign =
                "center";

            noResult.style.fontSize =
                "20px";

            noResult.style.margin =
                "30px";

            const menuGrid =
                document.querySelector(".menu-grid");

            if (menuGrid) {
                menuGrid.appendChild(noResult);
            }

        }

        noResult.style.display =
            "block";

    } else {

        if (noResult) {

            noResult.style.display =
                "none";

        }

    }

}


// ==========================================
// CATEGORY FILTER
// ==========================================

function filterFood(category, button) {

    const cards =
        document.querySelectorAll(".menu-card");


    const searchInput =
        document.getElementById("searchInput");

    if (searchInput) {

        searchInput.value = "";

    }


    const noResult =
        document.getElementById("no-food-result");

    if (noResult) {

        noResult.style.display =
            "none";

    }


    document
        .querySelectorAll(".category-btn")
        .forEach(function(btn) {

            btn.classList.remove(
                "active-category"
            );

        });


    if (button) {

        button.classList.add(
            "active-category"
        );

    }


    cards.forEach(function(card) {

        const cardCategory =
            card.getAttribute("data-category");


        if (
            category === "all" ||
            cardCategory === category
        ) {

            card.style.display = "";

        } else {

            card.style.display = "none";

        }

    });

}


// ==========================================
// ADD TO CART
// ==========================================

function setupAddToCart() {

    const forms =
        document.querySelectorAll(
            'form[action*="add-to-cart"]'
        );


    forms.forEach(function(form) {

        form.addEventListener(
            "submit",
            async function(event) {

                // Stop normal form submission
                event.preventDefault();


                try {

                    const formData =
                        new FormData(form);


                    const response =
                        await fetch(
                            form.action,
                            {
                                method: "POST",
                                body: formData
                            }
                        );


                    const data =
                        await response.json();


                    if (data.success) {

                        // Update cart count
                        const cartCount =
                            document.getElementById(
                                "cart-count"
                            );


                        if (cartCount) {

                            cartCount.innerText =
                                data.count;

                        }


                        // Show success message
                        showCartMessage(
                            "✅ " + data.message
                        );

                    } else {

                        showCartMessage(
                            "❌ " + data.message
                        );

                    }

                }
                catch (error) {

                    console.log(
                        "Add to cart error:",
                        error
                    );

                    showCartMessage(
                        "❌ Something went wrong."
                    );

                }

            }
        );

    });

}


// ==========================================
// CART SUCCESS POPUP
// ==========================================

function showCartMessage(message) {

    let popup =
        document.getElementById(
            "cart-message"
        );


    if (!popup) {

        popup =
            document.createElement("div");

        popup.id =
            "cart-message";


        popup.style.position =
            "fixed";

        popup.style.top =
            "90px";

        popup.style.right =
            "25px";

        popup.style.background =
            "#ffffff";

        popup.style.color =
            "#222";

        popup.style.padding =
            "15px 22px";

        popup.style.borderRadius =
            "10px";

        popup.style.boxShadow =
            "0 5px 20px rgba(0,0,0,0.2)";

        popup.style.zIndex =
            "9999";

        popup.style.fontSize =
            "16px";

        popup.style.fontWeight =
            "600";


        document.body.appendChild(
            popup
        );

    }


    popup.innerText =
        message;


    popup.style.display =
        "block";


    setTimeout(function() {

        popup.style.display =
            "none";

    }, 2000);

}


// ==========================================
// CART COUNT
// ==========================================

async function updateCartCount() {

    try {

        const response =
            await fetch("/cart-count");


        const data =
            await response.json();


        const cartCount =
            document.getElementById(
                "cart-count"
            );


        if (cartCount) {

            cartCount.innerText =
                data.count;

        }

    }
    catch (error) {

        console.log(
            "Cart count error:",
            error
        );

    }

}


// ==========================================
// PAGE LOAD
// ==========================================

document.addEventListener(
    "DOMContentLoaded",
    function() {

        updateCartCount();

        setupAddToCart();

    }
);