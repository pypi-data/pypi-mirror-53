

(function(globals) {

  var django = globals.django || (globals.django = {});

  
  django.pluralidx = function(n) {
    var v=n != 1;
    if (typeof(v) == 'boolean') {
      return v ? 1 : 0;
    } else {
      return v;
    }
  };
  

  /* gettext library */

  django.catalog = django.catalog || {};
  
  var newcatalog = {
    "(one more date)": [
      "(en dato mere)",
      "({num} datoer mere)"
    ],
    "All": "Alle",
    "An error has occurred.": "Der er sket en fejl.",
    "An error of type {code} occurred.": "Der er sket en fejl ({code}).",
    "Barcode area": "QR-kode-omr\u00e5de",
    "Cart expired": "Kurv udl\u00f8bet",
    "Check-in QR": "Check-in QR",
    "Close message": "Luk besked",
    "Comment:": "Kommentar:",
    "Confirming your payment \u2026": "Bekr\u00e6fter din betaling \u2026",
    "Contacting Stripe \u2026": "Kontakter Stripe \u2026",
    "Contacting your bank \u2026": "Kontakter din bank \u2026",
    "Copied!": "Kopieret!",
    "Count": "Antal",
    "Do you really want to leave the editor without saving your changes?": "Er du sikker p\u00e5 at du vil forlade editoren uden at gemme dine \u00e6ndringer?",
    "Error while uploading your PDF file, please try again.": "Fejl under upload af pdf. Pr\u00f8v venligt igen.",
    "Generating messages \u2026": "Opretter beskeder \u2026",
    "Group of objects": "Gruppe af objekter",
    "Marked as paid": "Markeret som betalt",
    "None": "Ingen",
    "Object": "Objekt",
    "Others": "Andre",
    "Paid orders": "Betalte bestillinger",
    "Placed orders": "Afgivne bestillinger",
    "Powered by pretix": "Drevet af pretix",
    "Press Ctrl-C to copy!": "Tryk Ctrl-C eller \u2318-C for at kopiere!",
    "Saving failed.": "Gem fejlede.",
    "Text object": "Tekstobjekt",
    "The PDF background file could not be loaded for the following reason:": "Baggrunds-pdf'en kunne ikke hentes af f\u00f8lgende grund:",
    "The items in your cart are no longer reserved for you.": "Varerne i din kurv er ikke l\u00e6ngere reserverede for dig.",
    "The items in your cart are reserved for you for one minute.": [
      "Varerne i din kurv er reserveret for dig i et minut.",
      "Varerne i din kurv er reserveret for dig i {num} minutter."
    ],
    "The request took to long. Please try again.": "Foresp\u00f8rgselen tog for lang tid. Pr\u00f8v venligst igen.",
    "Ticket design": "Billetdesign",
    "Total": "I alt",
    "Total revenue": "Oms\u00e6tning i alt",
    "Unknown error.": "Ukendt fejl.",
    "We are currently sending your request to the server. If this takes longer than one minute, please check your internet connection and then reload this page and try again.": "Din foresp\u00f8rgsel bliver sendt til serveren. Hvis det tager mere end et minut, s\u00e5 tjek din internetforbindelse, genindl\u00e6s siden og pr\u00f8v igen.",
    "We are processing your request \u2026": "Vi behandler din bestilling \u2026",
    "We currently cannot reach the server, but we keep trying. Last error code: {code}": "Vi kan ikke komme i kontakt med serveren, men pr\u00f8ver igen. Seneste fejlkode: {code}",
    "We currently cannot reach the server. Please try again. Error code: {code}": "Vi kan ikke komme i kontakt med serveren. Pr\u00f8v venligst igen. Fejlkode: {code}",
    "Your request arrived on the server but we still wait for it to be processed. If this takes longer than two minutes, please contact us or go back in your browser and try again.": "Din foresp\u00f8rgsel er under behandling. Hvis der g\u00e5r mere end to minutter, s\u00e5 kontakt os eller g\u00e5 tilbage og pr\u00f8v igen.",
    "Your request has been queued on the server and will now be processed. Depending on the size of your event, this might take up to a few minutes.": "Din foresp\u00f8rgsel er under behandling. Alt efter st\u00f8rrelsen af din event kan der g\u00e5 op til et par minutter.",
    "widget\u0004<a href=\"https://pretix.eu\" target=\"_blank\" rel=\"noopener\">event ticketing powered by pretix</a>": "<a href=\"https://pretix.eu\" target=\"_blank\" rel=\"noopener\">billetsystem drevet af pretix</a>",
    "widget\u0004Buy": "L\u00e6g i kurv",
    "widget\u0004Close": "Luk",
    "widget\u0004Close ticket shop": "Luk billetbutik",
    "widget\u0004Continue": "Forts\u00e6t",
    "widget\u0004FREE": "GRATIS",
    "widget\u0004Only available with a voucher": "Kun tilg\u00e6ngelig med en voucher",
    "widget\u0004Redeem": "Indl\u00f8s",
    "widget\u0004Redeem a voucher": "Indl\u00f8s voucher",
    "widget\u0004Reserved": "Reserveret",
    "widget\u0004See variations": "Vis varianter",
    "widget\u0004Sold out": "Udsolgt",
    "widget\u0004The cart could not be created. Please try again later": "Kurven kunne ikke oprettes. Pr\u00f8v igen senere",
    "widget\u0004The ticket shop could not be loaded.": "Billetbutikken kunne ikke hentes.",
    "widget\u0004Voucher code": "Voucherkode",
    "widget\u0004Waiting list": "Venteliste",
    "widget\u0004currently available: %s": "tilg\u00e6ngelig: %s",
    "widget\u0004from %(currency)s %(price)s": "fra %(currency)s %(price)s",
    "widget\u0004incl. %(rate)s% %(taxname)s": "inkl. %(rate)s% %(taxname)s",
    "widget\u0004minimum amount to order: %s": "minimumsantal: %s",
    "widget\u0004plus %(rate)s% %(taxname)s": "plus %(rate)s% %(taxname)s"
  };
  for (var key in newcatalog) {
    django.catalog[key] = newcatalog[key];
  }
  

  if (!django.jsi18n_initialized) {
    django.gettext = function(msgid) {
      var value = django.catalog[msgid];
      if (typeof(value) == 'undefined') {
        return msgid;
      } else {
        return (typeof(value) == 'string') ? value : value[0];
      }
    };

    django.ngettext = function(singular, plural, count) {
      var value = django.catalog[singular];
      if (typeof(value) == 'undefined') {
        return (count == 1) ? singular : plural;
      } else {
        return value.constructor === Array ? value[django.pluralidx(count)] : value;
      }
    };

    django.gettext_noop = function(msgid) { return msgid; };

    django.pgettext = function(context, msgid) {
      var value = django.gettext(context + '\x04' + msgid);
      if (value.indexOf('\x04') != -1) {
        value = msgid;
      }
      return value;
    };

    django.npgettext = function(context, singular, plural, count) {
      var value = django.ngettext(context + '\x04' + singular, context + '\x04' + plural, count);
      if (value.indexOf('\x04') != -1) {
        value = django.ngettext(singular, plural, count);
      }
      return value;
    };

    django.interpolate = function(fmt, obj, named) {
      if (named) {
        return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
      } else {
        return fmt.replace(/%s/g, function(match){return String(obj.shift())});
      }
    };


    /* formatting library */

    django.formats = {
    "DATETIME_FORMAT": "j. F Y H:i",
    "DATETIME_INPUT_FORMATS": [
      "%d.%m.%Y %H:%M:%S",
      "%d.%m.%Y %H:%M:%S.%f",
      "%d.%m.%Y %H:%M",
      "%Y-%m-%d %H:%M:%S",
      "%Y-%m-%d %H:%M:%S.%f",
      "%Y-%m-%d %H:%M",
      "%Y-%m-%d"
    ],
    "DATE_FORMAT": "j. F Y",
    "DATE_INPUT_FORMATS": [
      "%d.%m.%Y",
      "%Y-%m-%d"
    ],
    "DECIMAL_SEPARATOR": ",",
    "FIRST_DAY_OF_WEEK": 1,
    "MONTH_DAY_FORMAT": "j. F",
    "NUMBER_GROUPING": 3,
    "SHORT_DATETIME_FORMAT": "d.m.Y H:i",
    "SHORT_DATE_FORMAT": "d.m.Y",
    "THOUSAND_SEPARATOR": ".",
    "TIME_FORMAT": "H:i",
    "TIME_INPUT_FORMATS": [
      "%H:%M:%S",
      "%H:%M:%S.%f",
      "%H:%M"
    ],
    "YEAR_MONTH_FORMAT": "F Y"
  };

    django.get_format = function(format_type) {
      var value = django.formats[format_type];
      if (typeof(value) == 'undefined') {
        return format_type;
      } else {
        return value;
      }
    };

    /* add to global namespace */
    globals.pluralidx = django.pluralidx;
    globals.gettext = django.gettext;
    globals.ngettext = django.ngettext;
    globals.gettext_noop = django.gettext_noop;
    globals.pgettext = django.pgettext;
    globals.npgettext = django.npgettext;
    globals.interpolate = django.interpolate;
    globals.get_format = django.get_format;

    django.jsi18n_initialized = true;
  }

}(this));

