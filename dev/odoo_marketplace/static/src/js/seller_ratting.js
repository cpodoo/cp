/** @odoo-module **/
/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : https://store.webkul.com/license.html/ */
import { _t } from "@web/core/l10n/translation";
import { rpc } from "@web/core/network/rpc";
    $(document).ready(function() {
        $('.avg-rating-cir').percentcircle({
            animate : true,
            diameter : 130,
            guage: 6,
            coverBg: '#fff',
            bgColor: '#efefef',
            fillColor: '#FFC930',
            percentSize: '15px',
            percentWeight: 'normal'
        });
        $('.recommendation-cir').percentcircle({
            animate : true,
            diameter : 130,
            guage: 6,
            coverBg: '#fff',
            bgColor: '#efefef',
            fillColor: '#5bc0de',
            percentSize: '15px',
            percentWeight: 'normal'
        });
        $("#rating-star").rating({
            clearCaption: ('Not Rated'),
            starCaptions: {1: ("Poor"), 2: ("Ok"), 3: ("Good"), 4: ("Very Good"), 5: ("Excellent")},
            starCaptionClasses: {1: "badge badge-danger", 2: "badge badge-warning", 3: "badge badge-info", 4: "badge badge-primary", 5: "badge badge-success"},
        });


        $('#btn-create-review').on('click',function (e){
               var rate = $("#rating-star").val();
               var title = $("#title").val().trim();
               var review_summary = $("#summary").val().trim();
            if (rate<=0)
            {
                $("#submit-msg").empty();
                $("#submit-msg").html(_t(" Please add your rating !!!"));
                $("#submit-msg").addClass("alert-danger submit-error-msg fa fa-exclamation-triangle");
                $('#submit-msg').show();
            }
            else if(title == "")
            {
                $("#review-title-box").addClass("has-error");
                $("#submit-msg").html(_t(" Review title is required field."));
                $("#submit-msg").addClass("alert-danger submit-error-msg fa fa-exclamation-triangle");
                $('#submit-msg').show();
            }
            else if(review_summary == "")
            {
                $("#review-title-box").removeClass("has-error");
                $("#submit-msg").empty();
                $("#review-summary-box").addClass("has-error");
                $("#submit-msg").html(_t(" Review is required field."));
                $("#submit-msg").addClass("alert-danger submit-error-msg");
                $('#submit-msg').show();
            }
            else
            {
                $("#review-summary-box").removeClass("has-error alert-danger submit-error-msg");
                rpc("/seller/review/check",
                {
                    'seller_id':seller_id,
                })
                .then(function (result)
                {
                    if (jQuery.type(result) == "boolean")
                    {
                        $('#btn-create-review').addClass('disabled');
                        var button_add_reviewext = $('#btn-create-review').html()
                        $('#btn-create-review').html('<i class="fa fa-refresh fa-spin"></i> Posting...');
                        rpc("/seller/review", 
                        {
                            'seller_id':seller_id,
                            'stars':rate,
                            'title':title,
                            'review':review_summary,
                        })
                        .then(function (response)
                        {
                            $("#mp-review-form").trigger('reset');
                            if (response)
                            {
                                $("#submit-msg").html(response);
                                $("#submit-msg").removeClass("alert-danger alert-warning");
                                $("#submit-msg").addClass("alert-success submit-error-msg fa fa-check-circle");
                                setTimeout(function() {$('#submit-msg').hide()},3500);
                            }
                            else
                            {
                                $("#submit-msg").html(("  Your review has been submitted successfully. Thank you!"));
                                $("#submit-msg").removeClass("alert-danger alert-warning");
                                $("#submit-msg").addClass("alert-success submit-error-msg fa fa-check-circle");
                                setTimeout(function() {$('#submit-msg').hide()},3500);
                            }
                            $('#btn-create-review').removeClass('disabled');
                            $('#btn-create-review').html(button_add_reviewext);
                        });
                    }
                    else
                    {
                        $("#submit-msg").html(result);
                        $("#submit-msg").removeClass("alert-danger");
                        $("#submit-msg").addClass("alert-warning submit-error-msg fa fa-exclamation-triangle");
                    }
                });
            }
        });

        $(document).on('keyup', '#review-title-box',function()
        {
            $("#review-title-box").removeClass("has-error");
            $("#submit-msg").removeClass(" alert-danger submit-error-msg fa fa-exclamation-triangle fa-check-circle alert-success");
            $("#submit-msg").empty();
        });
        $(document).on('keyup', '#review-summary-box',function()
        {
            $("#review-summary-box").removeClass("has-error");
            $("#submit-msg").removeClass("alert-danger submit-error-msg fa fa-exclamation-triangle alert-warning fa-check-circle alert-success");
            $("#submit-msg").empty();
        });

        var sort_by = "recent";
        var filter_by = -1;
        var offset = 0;
        var seller_id =  parseInt($('#seller_all_review').find('input[type="hidden"][name="seller_id"]').first().val(),10);

        $('#mp-load-morebtn').on('click',function (e)
        {
            // var select_star = parseInt($('#select_star').val(),10);
            var total_seller_reviews = $('#total_seller_reviews').html();
            var limit =  parseInt($('#seller_all_review').find('input[type="hidden"][name="limit"]').first().val(),10);
            offset=offset+limit ;
            $("#mp-load-morebtn").hide();
            $("#mp-load-morebtn-loder").show();
            rpc("/seller/load/review", 
            {
                'seller_id':seller_id,
                'offset': offset,
                'limit': limit,
                'sort_by':sort_by,
                'filter_by':filter_by,
            })
            .then(function (result)
            {
                var $review =$(result);
                $review.appendTo('.mp-box-review');
                $("#mp-load-morebtn-loder").hide();
                $("#mp-load-morebtn").show();
            });


            rpc("/seller/load/review/count", 
            {
                'seller_id':seller_id,
                'offset': offset,
                'limit': limit,
                'sort_by':sort_by,
                'filter_by':filter_by,
            })
            .then(function (result)
            {
                if (result[0] > 0)
                    $('#viewed').text(offset+result[0]);
                if (total_seller_reviews == offset+result[0])
                    $('#mp-load-more-div').hide();
            });
        });

        // Code for updating reviews using nav-bar menus
        $('.review_filter_by a').click(function()
        {
            $('#filter_selected').text($(this).text());
            offset = 0;
            var select_star_offset = 0;
            filter_by = parseInt($(this).data("custom-value"));            
            var limit =  parseInt($('#seller_all_review').find('input[type="hidden"][name="limit"]').first().val(),10);
            var total_seller_reviews = $('#total_seller_reviews').html();
            $('.mp-box-review_loader').show();
            rpc("/seller/load/review", 
            {
                'seller_id':seller_id,
                'offset': 0,
                'limit': limit,
                'sort_by':sort_by,
                'filter_by':filter_by,
            })
            .then(function (result)
            {
                var $review =$(result);
                $('.mp-box-review').html($review);
                $('.mp-box-review_loader').hide();
            });
            rpc("/seller/load/review/count", 
            {
                'seller_id':seller_id,
                'offset': offset,
                'limit': limit,
                'sort_by':sort_by,
                'filter_by':filter_by,
            })
            .then(function (result)
            {
                $('#viewed').text(select_star_offset+result[0]);
                if (result[1] == select_star_offset+result[0])
                    $('#mp-load-more-div').hide();
                else
                    $('#mp-load-more-div').show();
                $('#total_seller_reviews').text(result[1]);
            });
        });

        $('.review_sort_by a').click(function(){
            $('#selected').text($(this).text());
          });

        $('#most_helpfulab').on('click',function (e)
        {
            offset = 0;
            sort_by = "most_helpful"
            var most_helpfulab_offset = 0;
            var limit =  parseInt($('#seller_all_review').find('input[type="hidden"][name="limit"]').first().val(),10);
            var total_seller_reviews = $('#total_seller_reviews').html();
            $("#most_recentab").removeClass("active-sort-tab");
            $("#most_helpfulab").addClass("active-sort-tab");
            $('.mp-box-review_loader').show();
            rpc("/seller/load/review", 
            {
                'seller_id':seller_id,
                'offset': most_helpfulab_offset,
                'limit': limit,
                'sort_by':sort_by,
                'filter_by':filter_by,
            })
            .then(function (result)
            {
                var $review =$(result);
                $('.mp-box-review').html($review);
                $('.mp-box-review_loader').hide();
            });
            rpc("/seller/load/review/count", 
            {
                'seller_id':seller_id,
                'offset': most_helpfulab_offset,
                'limit': limit,
                'sort_by':sort_by,
                'filter_by':filter_by,
            })
            .then(function (result)
            {
                if (result[0])
                    $('#viewed').text(most_helpfulab_offset+result[0]);
                if (result[1] == most_helpfulab_offset+result[0])
                    $('#mp-load-more-div').hide();
                else
                    $('#mp-load-more-div').show();
            });
        });

        $('#most_recentab').on('click',function (e)
        {
            offset = 0;
            sort_by = "recent"
            var most_recentab_offset = 0;
            var limit =  parseInt($('#seller_all_review').find('input[type="hidden"][name="limit"]').first().val(),10);
            var total_seller_reviews = $('#total_seller_reviews').html();
            $("#most_helpfulab").removeClass("active-sort-tab");
            $("#most_recentab").addClass("active-sort-tab");
            $('.mp-box-review_loader').show();
            rpc("/seller/load/review",
            {
                'seller_id':seller_id,
                'offset': 0,
                'limit': limit,
                'sort_by':sort_by,
                'filter_by':filter_by,
            })
            .then(function (result)
            {
                var $review =$(result);
                $('.mp-box-review').html($review);
                $('.mp-box-review_loader').hide();
            });
            rpc("/seller/load/review/count",
            {
                'seller_id':seller_id,
                'offset': most_recentab_offset,
                'limit': limit,
                'sort_by':sort_by,
                'filter_by':filter_by,
            })
            .then(function (result)
            {
                if (result[0])
                    $('#viewed').text(most_recentab_offset+result[0]);
                if (result[1] == most_recentab_offset+result[0])
                    $('#mp-load-more-div').hide();
                else
                    $('#mp-load-more-div').show();
            });
        });


        $("body").on('click', ".mp-sprite", function(e){
            var $review_box_bottom = $(this).closest('.seller-review-bottom');
            if ($(this).hasClass('mp-TopLeft'))
            {
                $(this).removeClass('mp-TopLeft');
                $(this).addClass('mp-BottomLeft');

                var seller_review_id =  parseInt($(this).closest('.seller_review_div').find("#seller_review_id").val(),10);
                var review_help = 1;
                rpc("/seller/review/help",
                {
                    'seller_review_id': seller_review_id,
                    'review_help': review_help
                })
                .then(function (result)
                {
                    if (result)
                    {
                        $review_box_bottom.find('.review_helpful').text(result[0]);
                        $review_box_bottom.find('.review_not_helpful').text(result[1]);
                    }
                });
                $('.seller_review_div .mp-BottomRight').addClass('mp-TopRight').removeClass('mp-BottomRight');
                return;
            }

            if ($(this).hasClass('mp-TopRight'))
            {
                $(this).removeClass('mp-TopRight');
                $(this).addClass('mp-BottomRight');
                var seller_review_id =  parseInt($(this).closest('.seller_review_div').find("#seller_review_id").val(),10);
                var review_help = -1;
                rpc("/seller/review/help",
                {
                    'seller_review_id': seller_review_id,
                    'review_help': review_help
                })
                .then(function (result)
                {
                    if (result)
                    {
                        $review_box_bottom.find('.review_not_helpful').text(result[1]);
                        $review_box_bottom.find('.review_helpful').text(result[0]);
                    }
                });
                $('.seller_review_div .mp-BottomLeft').addClass('mp-TopLeft').removeClass('mp-BottomLeft');
                return;
            }
            if ($(this).hasClass('mp-BottomLeft'))
            {
                $(this).removeClass('mp-BottomLeft');
                $(this).addClass('mp-TopLeft');
                var seller_review_id =  parseInt($(this).closest('.seller_review_div').find("#seller_review_id").val(),10);
                var review_help = 2;
                rpc("/seller/review/help",
                {
                    'seller_review_id': seller_review_id,
                    'review_help': review_help
                })

                .then(function (result)
                {
                    if (result)
                    {
                        $review_box_bottom.find('.review_helpful').text(result[0]);
                        $review_box_bottom.find('.review_not_helpful').text(result[1]);
                    }
                });
                return;
            }
            if ($(this).hasClass('mp-BottomRight'))
            {
                $(this).removeClass('mp-BottomRight');
                $(this).addClass('mp-TopRight');
                var seller_review_id =  parseInt($(this).closest('.seller_review_div').find("#seller_review_id").val(),10);
                var review_help = -2;
                rpc("/seller/review/help",
                {
                    'seller_review_id': seller_review_id,
                    'review_help': review_help
                })
                .then(function (result)
                {
                    if (result)
                    {
                        $review_box_bottom.find('.review_not_helpful').text(result[1]);
                        $review_box_bottom.find('.review_helpful').text(result[0]);
                    }
                });
                return;
            }
        });

        $('#recommend-yes').on('click',function (e){
            if(!$('#recommend-yes').hasClass("disabled")){
                var recommend_no = $("#recommend-no");
                var recommend_msg = $("#recommend-msg");
                var $this = $(this);
                rpc('/seller/recommend',
                {
                    'seller_id':seller_id,
                    "recommend_state":"yes"
                })
                .then(function (result)
                {
                    if(result){
                        if(typeof(result) == 'boolean') {
                            $this.removeClass("btn-info");
                            $this.addClass("disabled");
                            if(recommend_no.hasClass("disabled")){
                                recommend_no.removeClass("disabled");
                                recommend_no.addClass("btn-info");
                            }
                            recommend_msg.html("<p>Thank you!<br/>Your recommendation will be published soon.</p>")
                        }
                        else {
                            recommend_msg.html("<span class='alert-warning submit-error-msg fa fa-exclamation-triangle'>"+result+"</span>");
                        }
                    }
                });
            }
        });
        $('#recommend-no').on('click',function (e){
            if(!$('#recommend-no').hasClass("disabled")){
                var recommend_yes = $("#recommend-yes");
                var recommend_msg = $("#recommend-msg");
                var $this = $(this);
                rpc('/seller/recommend',
                {
                    'seller_id':seller_id,
                    "recommend_state":"no"
                })
                .then(function (result)
                {
                    if(result){
                        if(typeof(result) == 'boolean') {
                            $this.removeClass("btn-info");
                            $this.addClass("disabled");
                            if(recommend_yes.hasClass("disabled")){
                                recommend_yes.removeClass("disabled");
                                recommend_yes.addClass("btn-info");
                            }
                            recommend_msg.html("<p>Thank you!<br/>Your recommendation will be published soon.</p>")
                        }
                        else {
                            recommend_msg.html("<span class='alert-warning submit-error-msg fa fa-exclamation-triangle'>"+result+"</span>");
                        }
                    }
                });
            }
        });
        $('#open-review-tab').click(function(e){
            e.preventDefault();
            $('#shop-nav-tabs a[href="#rating_reviewab"]').tab('show');
            $('html,body').animate({scrollTop: $("#seller-info-pannel").offset().top},'slow');
        })
    });
    $("abbr.timeago").timeago();

