const formholder = $(".formholder");
const search = $(".search");
const year = $(".year");
const make = $(".make");
const model = $(".modal");
const engine = $(".engine");

$(document).on("change", () => {
  if (year.val() != "none" && make.val() != "none") {
    search.attr("disable", false);
  } else {
    search.attr("disabled", true);
  }
});
