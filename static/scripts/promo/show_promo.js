$(document).ready(function() {

    $('#filter-discount').on('change', function() {
        const filterValue = $(this).val();
        filterPromos(filterValue);
    });

    function filterPromos(filter) {
        $.ajax({
            url: '/promo/filter/', 
            type: 'GET',
            data: { filter: filter }, 
            success: function(data) {
                updatePromoList(data.promos);
            },
            error: function(error) {
                console.log('Error fetching filtered promos:', error);
            }
        });
    }

    function updatePromoList(promos) {
        const promoListContainer = $('.promo-container'); 
        promoListContainer.empty(); 

        if (promos.length === 0) {
            promoListContainer.append('<p class="text-center text-gray-700">Tidak ada promosi aktif saat ini.</p>');
            return;
        }

        promos.forEach(promo => {
            const endDate = new Date(promo.end_date);
            const options = { month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: 'numeric', hour12: true };
            const formattedDate = endDate.toLocaleString('en-US', options);
            promoListContainer.append(`
                <div class="promo-card bg-white border border-gray-300 rounded-lg shadow-lg p-4 transition-transform transform hover:scale-105" data-id="${promo.id}">
                    <h2 class="text-xl font-semibold text-gray-800">${DOMPurify.sanitize(promo.title)}</h2>
                    <p class="text-gray-600 mt-1">
                        ${DOMPurify.sanitize(promo.description).slice(0, 30)}...
                    </p>
                    <p class="font-bold text-gray-800 mt-2">Diskon: <span class="text-green-600">${DOMPurify.sanitize(promo.discount_percentage)}%</span></p>
                    <p class="font-bold text-gray-800">Kode Promo: <span class="bg-gray-200 border border-gray-400 rounded px-2 py-1 text-red-500 font-mono">${DOMPurify.sanitize(promo.promo_code)}</span></p>
                    <p class="font-bold text-gray-800">Valid Hingga: <span class="text-gray-500">${formattedDate}</span></p>
                    <button class="promo-detail-button text-blue-600 hover:underline" data-id="${promo.id}">Detail</button>
                </div>
            `);
        });
    }

    $(document).on('click', '.promo-detail-button', function() {
        const promoId = $(this).data('id'); 
        
        $.ajax({
            url: '/promo/get/' + promoId + '/', 
            type: 'GET',
            success: function(data) {
                console.log(data); 
                
                $('#promoDetailTitle').text(DOMPurify.sanitize(data.title));
                
                const startDate = new Date(data.start_date).toLocaleDateString();
                const endDate = new Date(data.end_date).toLocaleDateString();
                
                $('#promoDetailContent .promo-description').text(DOMPurify.sanitize(data.description));
                $('#promoDetailContent .promo-code').text(DOMPurify.sanitize(data.promo_code));
                $('#promoDetailContent .promo-discount').text(`${DOMPurify.sanitize(data.discount_percentage)}%`);
                $('#promoDetailContent .promo-dates').text(`${startDate} - ${endDate}`);

                $('#promoDetailModal').removeClass('hidden');
            },
            error: function(error) {
                console.log('Error fetching promo details:', error); 
            }
        });
    });

    $('#backPromoDetailModal').on('click', function() {
        $('#promoDetailModal').addClass('hidden');
    });

    $('#createPromoButton').click(function() {
        $('#promoForm').slideDown();
        $(this).hide();
    });

    $('#savePromoButton').on('click', function(e) {
        e.preventDefault();
        const formData = $('#promoForm').serialize();
        const promoId = $('#promo_id').val();
        const url = promoId ? '/promo/update/' + promoId + '/' : '/promo/create/';
    
        $.ajax({
            type: 'POST',
            url: url,
            data: formData,
            headers: {
                'X-CSRFToken': $('meta[name="csrf-token"]').attr('content')
            },
            success: function(response) {
                if (response.status === 'success' || response.success) {
                    location.reload(); 
                } else {
                    alert('Error: ' + JSON.stringify(response.errors));
                }
            },
            error: function(xhr) {
                const errors = xhr.responseJSON.errors || {};

                $('.error-message').text('');

                for (const [field, messages] of Object.entries(errors)) {
                    const inputField = $(`#${field}`);
                    inputField.next('.error-message').text(DOMPurify.sanitize(messages.join(', ')));
                }
    
                $('#promoForm').show();
            }
        });
    });
    
    $(document).on('click', '.edit-promo', function() {
        var promoId = $(this).data('id');

        $.ajax({
            type: 'GET',
            url: '/promo/get/' + promoId + '/',
            success: function(data) {
                $('#promo_id').val(data.id);
                $('#title').val(data.title);
                $('#description').val(data.description);
                $('#discount_percentage').val(data.discount_percentage);
                $('#promo_code').val(data.promo_code);
                $('#start_date').val(data.start_date);
                $('#end_date').val(data.end_date);
                $('#promoForm').slideDown(); 
                $('#createPromoButton').hide(); 
                $('#savePromoButton').text('Update Promo'); 
            },
            error: function(xhr) {
                const errors = xhr.responseJSON.errors || {};

                $('.error-message').text('');

                for (const [field, messages] of Object.entries(errors)) {
                    const inputField = $(`#${field}`);
                    if (inputField.length) {
                        inputField.next('.error-message').text(DOMPurify.sanitize(messages.join(', ')));
                    }
                }

                alert('Error fetching promo data: ' + xhr.responseText);
            }
        });
    });

    $(document).on('click', '.delete-promo', function() {
        var promoId = $(this).data('id');
    
        var csrfToken = $('meta[name="csrf-token"]').attr('content');
    
        Swal.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: '/promo/delete/' + promoId + '/',
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken
                    },
                    data: { id: promoId },
                    success: function(response) {
                        Swal.fire(
                            'Deleted!',
                            'Your promo has been deleted.',
                            'success'
                        ).then(() => {
                            location.reload(); 
                        });
                    },
                    error: function(xhr, status, error) {
                        Swal.fire(
                            'Error!',
                            'There was a problem deleting the promo.',
                            'error'
                        );
                    }
                });
            }
        });
    });

    $('#backButton').on('click', function() {
        $('#promoForm').slideUp();
        $('#createPromoButton').show(); 
        $('#promo_id').val('');
        $('#promoForm')[0].reset(); 
        $('#savePromoButton').text('Save Promo'); 
        $('.error-message').text('');
    });

});

