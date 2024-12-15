<!doctype html>
<html>
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css" integrity="sha384- GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous">
<link rel="icon" href="header/logoo.png" sizes="32x32" type="image/png">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<style>
    header {
        padding: 25px 10px;
        display: flex;
        justify-content: space-between;
        background-color: #f3f3f3;
    }
    .logo {
        align-self: center;
    }
    .block0 {
        display: flex;
        justify-content: center;
    }
    .imgheader {
        width: 2.5vw;
        height: auto;
        align-self: center;
    }
    button {
        padding: 7px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
    button:focus, button:active {
        outline: none;
    }
    .navitem {
        display: flex;
        justify-content: center;
    }
</style>
</head>
<body>
<header>
    <div class="logo">
        <a href="index.php"><img src="header/logo.png" alt="PharmaInsight" width="35%" height="35%"></a>
    </div>
    <form id="searchForm">
    <div class="block0">
        <div class="navitem">
            <input type="text" id="inputBox" style="display:none;" placeholder="search?">
        </div>
        <div class="navitem">
            <button type="button" onclick="searchfunc(event)"><img src="header/search.png" alt="search" width="30%" height="30%" class="imgheader"></button>
        </div>
    </div>
    </form>
</header>

<script>
var x = 0;

function searchfunc(event) {
    event.preventDefault();  // 阻止表單提交，避免重新載入頁面
    
    var inputBox = document.getElementById("inputBox");

    if (x === 0) {
        x = 1;
        inputBox.style.display = "block"; // 顯示輸入框
    } else {
        x = 0;
        var query = inputBox.value.trim();
        if (query) {
            inputBox.style.display = "none"; 

            fetch("http://localhost:5000/drug-side-effects?query=" + query)
                .then(response => {
                    if (!response.ok) {
                        throw new Error("沒有找到該藥物的資訊耶哭哭" );
                    }
                    return response.json();
                })
                .then(data => {
                    console.log("Received response:", data);

                    var resultDiv = document.getElementById("result");
                    if (!resultDiv) {
                        resultDiv = document.createElement('div');
                        resultDiv.id = 'result';
                        document.body.appendChild(resultDiv);
                    }
                    if (data.error) {
                        resultDiv.innerHTML = `<h3>Error</h3><p>${data.error}</p>`;
                    } else {
                        resultDiv.innerHTML = ` 
                            <h3>${data.title}</h3>
                            <p><strong>Drug Name:</strong> ${data.drug_name}</p>
                            <p><strong>Description:</strong> ${data.description.join('<br>')}</p>
                            ${data.side_effects.length > 0 ? 
                                `<h4>Possible Side Effects:</h4>
                                 <ul>
                                    ${data.side_effects.map(effect => `<li>${effect}</li>`).join('')}
                                 </ul>` 
                                : '<p>No side effects information available.</p>'}
                        `;
                    }
                })
                .catch(error => {
                    console.error("Error:", error);

                    var resultDiv = document.getElementById("result");
                    if (!resultDiv) {
                        resultDiv = document.createElement('div');
                        resultDiv.id = 'result';
                        document.body.appendChild(resultDiv);
                    }
                    resultDiv.innerHTML = `<h3>No results found for: ${query}</h3><p>${error.message}</p>`; // Show the search query
                });
        } else {
            inputBox.style.display = "none"; 
        }
    }
}

</script>
</body>
</html>

