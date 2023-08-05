
NewReviewModal = function (params) {
    var self = this;
    this.url = params.url;
    this.$target = params.$target;

    this.$target.click(function () {
        $.get(self.url, function (response) {
            var $modal = $(response),
                $splash = $modal.find('[data-role=splash]');

            $('body').append($modal);

            $modal.modal('show');

            $modal.on('hidden.bs.modal', function (e) {
                $modal.remove();
            });

            $modal.find('form').submit(function (e) {

                e.preventDefault();

                $splash.show();

                $(this).ajaxSubmit({
                    success: function(response) {
                        $modal.modal('hide');
                        $.notify({message: response}, {type: 'success'});
                    },
                    error: function(response) {
                        $modal.find('.modal-body').html(response.responseText);
                        $splash.hide();
                    }
                });
            });

        });
    });
};
