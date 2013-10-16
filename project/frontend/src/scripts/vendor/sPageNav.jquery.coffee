# Reference jQuery
$ = jQuery

# Adds plugin object to jQuery
$.fn.extend
  # Change sPageNav to your plugin's name.
  sPageNav: (options) ->
    # Default settings
    settings =
      navLink: 'a'
      animateNav: false
      debug: false

    # Merge default settings with options.
    settings = $.extend settings, options

    # Simple logger.
    log = (msg) ->
      console?.log msg if settings.debug

    # utility functions
    getElemStartEndPosition = (jqObj) ->
      console.log jqObj.innerHeight() if DEBUG
      start = jqObj.offset().top
      dimensions = 
        start: start
        end: start + jqObj.innerHeight()

    updateElemStartEndPosition = (obj) ->
      obj.pageBoundry = getElemStartEndPosition(obj.selector)

    getWindowCenterPosition = ->
      # get center of display position
      widowCenter = $(window).scrollTop() + ($(window).innerHeight() / 2)

    # debounce for resize and scroll functions
    debounce = (func, threshold, execAsap) ->
      timeout = null
      (args...) ->
        obj = this
        delayed = ->
          func.apply(obj, args) unless execAsap
          timeout = null
        if timeout
          clearTimeout(timeout)
        else if (execAsap)
          func.apply(obj, args)
        timeout = setTimeout delayed, threshold || 100


    @each () ->
      navigation = $(@)
      navLinks = $(@).find(settings.navLink)

      pages = navLinks.map (index, element) ->
        $element = $(element)
        $page = $($element.attr('href'))
        page = 
          link: $element
          selector: $page 
          pageBoundry: getElemStartEndPosition($page)

        calculatePageSize = ->
          updateElemStartEndPosition(page)

        calculateActivePage = ->
          # set active page
          isPageActuve = page.pageBoundry.start < getWindowCenterPosition() < page.pageBoundry.end

        hideMobileNav = ->
          #remove active class from nav on mobiles
          $target = $('[data-role="promo-nav"]').removeClass('is-active')

          if isPageActuve
            page.link.addClass('is-active')  
          else
            page.link.removeClass('is-active')

        setActiveOnClick = (event) ->
          event.preventDefault()
          navigation.find(settings.navLink).removeClass('is-active')
          $(event.currentTarget).addClass('is-active')
          console.log 'click' if DEBUG


        $(window).on 'resize.sPageNav', debounce(calculatePageSize, 500)
        $(window).on 'scroll.sPageNav', debounce(calculateActivePage, 200)
        $(window).on 'touchmove.sPageNav', debounce(hideMobileNav, 200)
        $(page.link).on 'click.sPageNav', setActiveOnClick


        return page
