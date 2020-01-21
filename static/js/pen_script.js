// quick search regex
var qsRegex;
var buttonFilter;

// The Isotope methods called here are so that the buttons within the seachgrid or any grid are positioned
// using the css that is present in my css files. Earlier, it would inherit the default layout mode of the isotope
// object which would mess with button positioning.
Isotope.Item.prototype._create = function() {
  // assign id, used for original-order sorting
  this.id = this.layout.itemGUID++;
  // transition objects
  this._transn = {
    ingProperties: {},
    clean: {},
    onEnd: {}
  };
  this.sortData = {};
};

Isotope.Item.prototype.layoutPosition = function() {
  this.emitEvent( 'layout', [ this ] );
};

Isotope.prototype.arrange = function( opts ) {
  // set any options pass
  this.option( opts );
  this._getIsInstant();
  // just filter
  this.filteredItems = this._filter( this.items );
  // flag for initalized
  this._isLayoutInited = true;
};

// layout mode that does not position items
Isotope.LayoutMode.create('none');

var $grid = $('.grid').isotope({
  itemSelector: '.grid-item',
  layoutMode: 'fitRows',
  filter: function() {
    var $this = $(this);
    var searchResult = qsRegex ? $this.text().match( qsRegex ) : true;
    var buttonResult = buttonFilter ? $this.is( buttonFilter ) : true;
    // console.log(buttonResult);
    return searchResult && buttonResult;
  }
});

var $searchgrid = $('#searchgrid').isotope({
  itemSelector: '.search-item',
  layoutMode: 'none',
  filter: function() {
    var $this = $(this);
    var searchResult = qsRegex ? $this.text().match(qsRegex) : true;
    // console.log(searchResult);
    return searchResult;
  }
});

// init Isotope
var $optiongrid = $('.option-grid').isotope({
  itemSelector: '.grid-item',
  layoutMode: 'fitRows',
  filter: function() {
    var $this = $(this);
    var buttonResult = buttonFilter ? $this.is( buttonFilter ) : true;
    // console.log(buttonResult);
    return buttonResult;
  }
});

$('#filters').on( 'click', 'button', function() {
  /* don't declare the buttonFilter below as a var. Because I guess it overwrites the variable of var used in the
  * initialization of the grid isotope. If you declare it as a var you'll see that the filtering won't occur. This is
  * because, the filter function in the isotope method attached to grid doesn't take any parameters. It uses the global
  * variable buttonFilter to get the filtered items and store it in buttonResult. However, when you declare the var
  * buttonFilter here, I guess it becomes a local variable that no longer modifies the previously defined global variable
  * and so there will be no changes to the filtered options. The codepen shows this declared as a var and still works
  * but I don't understand how. */
  buttonFilter = $( this ).attr('data-filter');
  $optiongrid.isotope();
  $grid.isotope();
});

// use value of search field to filter
var $quicksearch = $('#quicksearch').keyup( debounce( function() {
  qsRegex = new RegExp( $quicksearch.val().replace('\\','\\\\'), 'gi' );
  // console.log(qsRegex);
  $grid.isotope();
  $searchgrid.isotope();
}) );


  // change is-checked class on buttons
$('.single-sel-group').each( function( i, buttonGroup ) {
  var $buttonGroup = $( buttonGroup );
  $buttonGroup.on( 'click', 'button', function() {
    $buttonGroup.find('.is-checked').removeClass('is-checked');
    $( this ).addClass('is-checked');
  });
});


// debounce so filtering doesn't happen every millisecond
function debounce( fn, threshold ) {
  var timeout;
  threshold = threshold || 100;
  return function debounced() {
    clearTimeout( timeout );
    var args = arguments;
    var _this = this;
    function delayed() {
      fn.apply( _this, args );
    }
    timeout = setTimeout( delayed, threshold );
  };
}