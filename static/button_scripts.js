
$ (document).ready(function(){

function collectData() {
    let filters_arr = [];
    let loc = $("#locations-id").val();
    let source = $("#source-id").val();
    let home_type = $("#apartment-type-id").val();
    let size = $("#size-id").val();
    let price = $("#price-id").val();

    if (loc) {
    filters_arr.push(`location=${loc}`);
    }
    if (source) {
    filters_arr.push(`source_name=${source}`);
    }
    if (home_type) {
    filters_arr.push(`home_type=${home_type}`);
    }
    if (size) {
    filters_arr.push(`home_size=${size}`);
    }
    if (price) {
    filters_arr.push(`price=${price}`);
    }
    return filters_arr;
}

function generateURL(downloadURL=false) {
    let filters = collectData().join("&");
    let pathname = location.pathname;
    if (downloadURL) {
    pathname = pathname.replace("/", "/download-");
    }
    let new_url = `${location.origin}${pathname}?${filters}`;
    return new_url;
}

$("#filter-btn").on("click", function(){
    let generatedURL = generateURL(downloadURL=false);
    location.href = generatedURL;
});

$("#download-btn").on("click", function(){
    let generatedURL = generateURL(downloadURL=true);
    location.href = generatedURL;
});

});