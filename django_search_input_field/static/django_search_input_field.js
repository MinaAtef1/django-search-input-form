function markMatch(text, term) {
	// Find where the match is
	var match = text.toUpperCase().indexOf(term.toUpperCase());

	var $result = $('<span></span>');

	// If there is no match, move on
	if (match < 0) {
		return $result.text(text);
	}

	// Put in whatever text is before the match
	$result.text(text.substring(0, match));

	// Mark the match
	var $match = $('<span class="select2-rendered__match"></span>');
	$match.text(text.substring(match, match + term.length));

	// Append the matching text
	$result.append($match);

	// Put in whatever is after the match
	$result.append(text.substring(match + term.length));

	return $result;
}
function search_input_field_init() {
	var query_text = '';
    console.log('search_input_field_init');
	let url = $('#django-search-url').attr('url');
	let search_fields = $('.select2-search-query');

	for (let i = 0; i < search_fields.length; i++) {
		const element = search_fields[i];
		$(element).select2({
			width: 'resolve',
			allowClear: true,
			placeholder: 'search',
			templateResult: function (item) {
				// No need to template the searching text
				if (item.loading) {
					return item.text;
				}

				var term = query_text || '';
				var $result = markMatch(item.text, term);

				return $result;
			},
			ajax: {
				url: url,
				dataType: 'json',
				delay: 1000,
				data: function (params) {
					query_text = params.term;
					search_field = $(element).attr('search_field');
					// get all attrs that start with function_filters
					var function_filters = {};
					$.each($(element).get(0).attributes, function (index, attr) {
						if (attr.name.startsWith('function_filters')) {
							function_filters[attr.name] = attr.value;
						}
					});
					return {
						q: params.term, // search term
						search_field: search_field,
						...function_filters,
						query_name: $(this).attr('query_function'),
					};
				},
				processResults: function (data, params) {
					return {
						results: data
					};
				},
				cache: true,
			},
			minimumInputLength: element.getAttribute('min_search_length'),
		});
		$(element).on('select2:select', function (e) {
			
			var data = e?.params?.data?.fields_data;
			// get all input that has related_search_input_id = {{ widget.attrs.id }}
			var related_search_input = $(`input[related_search_input_id=${element.id}]`);
			// for each input, get the value of related_field and set it to the value of the input
			related_search_input.each(function (index, element) {
				var related_field = $(element).attr('related_field');
				
				$(element).val(data[related_field]);
			});
			console.log(data);
		});
	}
}
function search_input_field_destroy() {
    $('.select2-search-query').select2('destroy');
    $('.select2-search-query').off('select2:select');
}
$(document).ready(function () {
    search_input_field_init();
});

// opserver the dom for new elements
var observer = new MutationObserver(function (mutations) {
    mutations.forEach(function (mutation) {
        // get the added nodes that has the class select2-search-query
        var added_nodes = $(mutation.addedNodes).find('.select2-search-query');
        // if the added nodes has the class select2-search-query, destroy the select2 and reinit
        if (added_nodes.length > 0) {
            console.log(added_nodes.length > 0);
            search_input_field_init();
        }
    });
});
var config = { childList: true, subtree: true };
observer.observe(document, config);
