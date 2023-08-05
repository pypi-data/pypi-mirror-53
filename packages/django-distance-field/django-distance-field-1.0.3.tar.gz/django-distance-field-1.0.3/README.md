# ![Squarehost Logo](https://www.squarehost.co.uk/static/fake/media/favicons/apple-touch-icon-76x76.png) Django Distance Field

92% Unit Testing Coverage
<https://bitbucket.org/squarehost/django-distance-field.git>

***

(C) 2018 Squarehost Ltd. <http://www.squarehost.co.uk>

Ian Shurmer (ian@squarehost.co.uk)

***

## What is it?

Django Distance Field is a simple extension to Django's GIS fields to allow registration of a distance/measurement field within a model. Data within this field can then be converted using Django's "D" objects, and filtered using standard Django queryset functionality. 

It doesn't need a GIS enabled database or extension installed. It should work with Django version 1.7 and above.

## What does that mean?

Put simply, you can add a distance field which allows the user to enter a measurement using a large variety of units. This distance will then be converted to a standard unit format (for example, metres), and stored in the database. The user's specified units are also stored, and when the measurement retrieved, automatically converted into these to be displayed.

## Eh?

Well, how about some psuedo-code? Here's how you might use the API:

```python
In [1]: from mymodels.model import ModelWithWidthHeight

In [2]: from distance import D

In [3]: inst = ModelWithWidthHeight( )

In [4]: inst.width = "10m"

In [5]: inst.width
Out[5]: D(m=10.0)

In [6]: inst.height = "10in"

In [7]: inst.height
Out[7]: D(inch=10.0)

In [8]: inst.width > inst.height
Out[8]: True

In [9]: inst.height.m
Out[9]: 0.254
```

## Is that it? Yawn...

Wait, there's more! You can also filter querysets directly using either D objects or strings, with all your usual Django API niceness:

```python
In [1]: from mymodels.model import ModelWithWidthHeight

In [2]: from distance import D

In [3]: ModelWithWidthHeight.objects.filter(width__lte="10m")
Out[3]: <QuerySet [<ModelWithWidthHeight: ModelWithWidthHeight object (1)>]>

In [4]: ModelWithWidthHeight.objects.filter(width__lt="10m")
Out[4]: <QuerySet []>

In [5]: ModelWithWidthHeight.objects.filter(width__lte="1000cm")
Out[5]: <QuerySet [<ModelWithWidthHeight: ModelWithWidthHeight object (1)>]>

In [6]: ModelWithWidthHeight.objects.filter(width__lte="999cm")
Out[6]: <QuerySet []>

In [7]: ModelWithWidthHeight.objects.filter(width__lte="1000cm", height__gt=D(inch=9))
Out[7]: <QuerySet [<ModelWithWidthHeight: ModelWithWidthHeight object (1)>]>
```

## Okay, that looks a *little* more useful. What about forms and widgets?

Using a DistanceField automatically results in a standard CharField being included within the form, *BUT* with relevant validators applied to ensure that the system recognises the units, and throws a ValidationError if not.

The field data is then automatically parsed to the D object and stored in the database accordingly.

## What units do you recognise?

Along with Django's default units we have a couple of others thrown in (for example, [Rack Units/U](https://en.wikipedia.org/wiki/Rack_unit)), meaning current support is as follows:

 * Chain, Chain Benoit, Chain Sears, British Chain Benoit, British Chain Sears, British Chain Sears Truncated, Cm, British Ft, British Yd, Clarke Ft, Clarke Link, Fathom, Ft, German M, Gold Coast Ft, Indian Yd, Inch, Km, Link, Link Benoit, Link Sears, M, Mi, Mm, Nm, Nm Uk, Rod, Sears Yd, Survey Ft, Um, Yd, U

You can also add units if you so desire - simply call the distance.register_units method with your unit alias as keyword arguments, and the number of units *in metres* as the keyword value. For example:

```python
In [1]: import distance

In [2]: distance.register_units(my_unit=0.5, my_other_unit=2)

In [3]: distance.D(my_unit=10).m
Out[3]: 5.0

In [4]: distance.D(my_unit=10).inch
Out[4]: 196.8503937007874

In [5]: distance.D(my_other_unit=10).m
Out[5]: 20.0
```

You should probably do that somewhere like your app ready methods.

## What about aliases? You say "inch", I say '"'

We have a variety of aliases already specified within the D class:

|Actual Unit|Alias|
|-----------|-----|
|british_chain_benoit|British chain (Benoit 1895 B)|
|british_chain_sears_truncated|British chain (Sears 1922 truncated)|
|british_chain_sears|British chain (Sears 1922)|
|british_ft|British foot (Sears 1922)|
|british_ft|British foot|
|british_yd|British yard (Sears 1922)|
|british_yd|British yard|
|chain_benoit|Chain (Benoit)|
|chain_sears|Chain (Sears)|
|clarke_ft|Clarke\'s Foot|
|clarke_link|Clarke\'s link|
|cm|centimeter|
|ft|\'|
|ft|Foot (International)|
|ft|foot|
|german_m|German legal metre|
|gold_coast_ft|Gold Coast foot|
|inch|"|
|inch|inches|
|inch|in|
|indian_yd|Indian yard|
|indian_yd|Yard (Indian)|
|km|kilometer|
|km|kilometre|
|link_benoit|Link (Benoit)|
|link_sears|Link (Sears)|
|mi|mile|
|mm|millimeter|
|mm|millimetre|
|m|meter|
|m|metre|
|nm_uk|Nautical Mile (UK)|
|nm|Nautical Mile|
|sears_yd|Yard (Sears)|
|survey_ft|U.S. Foot|
|survey_ft|US survey foot|
|um|micrometer|
|um|micrometre|
|u|ru|
|yd|yard|

As we're not *too* picky, the aliases are case-insensitive.

## My alias isn't there?

Well, as with units, you can add your own. Keyword argument keys should be your new alias, with the value the existing units:

```python
In [1]: import distance

In [2]: distance.register_aliases(feet="ft")

In [3]: distance.D(feet=10)
Out[3]: D(ft=10.0)
```

## How does it work then?

When you create a DistanceField in your model, it also has a default unit (metres unless you change it through the unit kwarg). Any distances passed to this unit field are converted into this standard unit, before being saved into the database as a decimal in much the same way as a DecimalField.

### But you said it will remember my units? How?

Glad you asked. Optionally, although if you don't add it we can't remember your units, for each DistanceField you add you should also add a DistanceUnitField, and tell your DistanceField about it. The DistanceUnitField is a simple CharField, which is automatically populated depending on the units specified in your DistanceField.

You don't need to worry about this field, simply creating it in your model and pointing the DistanceField to it is all you need to do. It's not editable, and you don't need to change it.

## Okay, I'm sold. Well, sold enough to download and test an MIT-licensed library anyway. How do I use it?

You can install either directly via PyPi (pip install django-distance-field), or checkout from our Git repo: <https://bitbucket.org/squarehost/django-distance-field.git>

Usage is straightforward. As it's only a field, you don't need to add to your INSTALLED_APPS, although you can do so if you wish to run tests.

In your models.py file, create the DistanceField according to your requirements:

```python

from distance import DistanceField, DistanceUnitField

class ModelWithWidthHeight(models.Model):
	width = DistanceField(unit='m', unit_field='width_units')
	height = DistanceField(unit='in', unit_field='height_units')

	width_units = DistanceUnitField( )
	height_units = DistanceUnitField( )
```

DistanceField will also respect standard Django DecimalField options, such as ```blank```, ```null```, ```max_digits```, and ```decimal_places```. Bear in mind that the field will actually be stored in the *unit* you specify, so you might want to change the max_digits and precision depending on your requirements.

Also, bearing in mind that your units may well be converted to all other weird and wonderful units, you may want a couple of extra decimal places to try and reduce the occurrence of any strange rounding errors.

Default ```unit``` is m (metres), ```max_digits``` is 14, and ```decimal_places``` is 6.