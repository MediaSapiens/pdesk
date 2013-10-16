window.Application = {}
Application.MOBILE_VIEWPORT_POINT = 639 # same value shood be used in styles

$ ->
	console.log 'hello not again' if DEBUG
	Application.initSmoothScroll('[data-action="smooth-scroll"]')
	Application.initBlocksScroll()
	Application.initPressPopup()
	Application.initMobileNav()
	Application.initAddToCart()

	# $('.button').click (event)->
	# 	event.preventDefault()
	# 	$(event.currentTarget).addClass('is-ok-status')


Application.initSmoothScroll = (selector) ->
	console.log selector if DEBUG
	$('body').on 'click', selector, (event) ->
		event.preventDefault()

		elem = $(event.currentTarget)
		target = elem.attr('href')
		targetPosition = $('body').find(target).offset()

		$("html, body").animate({scrollTop: targetPosition.top}, 600)


Application.initFixedHeader = (selector) ->
	# console.log 'initFixedHeader' if DEBUG

	$elem = $(selector)
	elemTop = $elem.offset().top
	fixedStatus = off

	navScroll = (event) ->
		top = $(window).scrollTop()
		if top > elemTop and fixedStatus is off
			fixedStatus = on
			$elem.addClass('is-fixed')
		else if top < elemTop and fixedStatus is on
			fixedStatus = off
			$elem.removeClass('is-fixed')
				
		# if $(window).scrollTop() > elemTop 
		# 	elem.addClass('is-fixed')
		# else 
		# 	elem.removeClass('is-fixed')

	$(window).on 'scroll', navScroll


Application.initBlocksScroll = ->
	console.log 'initBlocksScroll' if DEBUG
	
	# init iscroll for tablets and pc for each media-box element
	if $(window).width() > Application.MOBILE_VIEWPORT_POINT
		$('.iscroller').each ->
			scroller = new iScroll @,
				bounce: true
				scrollbarClass: 'iscroll-bar'
			# scroller = new FTScroller @,
				# scrollingX: false



Application.initPressPopup = ->
	$('body').on 'click', '[data-action="open-close-feed-popup"]', (event) ->
		event.preventDefault()
		console.log 'open-close popup' if DEBUG
		$elem = $(event.currentTarget)
		$elem.closest('[data-role="feed-popup"]').toggleClass('is-active')
				

# show mobile nav on mobile device on click
Application.initMobileNav = ->
	$('body').on 'click', '[data-role="promo-nav-toggle"]', (event) ->
		event.preventDefault()
		$target = $('[data-role="promo-nav"]').toggleClass('is-active')
		console.log 'initMobileNav' if DEBUG


Application.initAddToCart = ->
	okMesageDelay = 1000

	$('body').on 'click', '[data-action="add-to-cart"]', (event) ->
		event.preventDefault()
		$(event.currentTarget)
			.addClass('is-ok-status')
			.find('.button__text--confirm-message')
			.delay(okMesageDelay)
			.fadeOut()
