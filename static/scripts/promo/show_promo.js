$(document).ready(function() {

    $(document).on('click', '.promo-detail-button', function() {
        const promoId = $(this).data('id'); 
        
        $.ajax({
            url: '/promo/get/' + promoId + '/', 
            type: 'GET',
            success: function(data) {
                console.log(data); 
                
                $('#promoDetailTitle').text(data.title);
                
                const startDate = new Date(data.start_date).toLocaleDateString();
                const endDate = new Date(data.end_date).toLocaleDateString();
                
                $('#promoDetailContent .promo-description').text(data.description);
                $('#promoDetailContent .promo-code').text(data.promo_code);
                $('#promoDetailContent .promo-discount').text(`${data.discount_percentage}%`);
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
        var formData = $('#promoForm').serialize();
        var promoId = $('#promo_id').val(); 

        var url = promoId ? '/promo/update/' + promoId + '/' : '/promo/create/';

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
                var errors = xhr.responseJSON.errors || {};
                var errorMessagesDiv = $('#error-messages'); // Asumsi Anda sudah membuat div ini
                errorMessagesDiv.empty(); // Kosongkan pesan sebelumnya

                for (const [field, messages] of Object.entries(errors)) {
                    messages.forEach(message => {
                        errorMessagesDiv.append('<p>' + message + '</p>'); // Tambahkan pesan kesalahan
                    });
                }

                errorMessagesDiv.show(); 
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
                alert('Error fetching promo data: ' + xhr.responseText);
            }
        });
    });

    $(document).on('click', '.delete-promo', function() {
        var promoId = $(this).data('id');

        // Use SweetAlert2 for a confirmation dialog
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
                // Proceed with the AJAX call if confirmed
                $.ajax({
                    url: '/promo/delete/' + promoId + '/',
                    method: 'POST',
                    data: { id: promoId },
                    success: function(response) {
                        // Handle success (e.g., show a success message)
                        Swal.fire(
                            'Deleted!',
                            'Your promo has been deleted.',
                            'success'
                        ).then(() => {
                            location.reload(); // Refresh the page
                        });
                    },
                    error: function(xhr, status, error) {
                        // Handle error (e.g., show an error message)
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
    });

    
});



