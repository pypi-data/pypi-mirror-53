# Advocate Python SDK

This SDK is for developing tools on/with the Advocate live-streaming platform.  Currently, it is primarily used for creating Dynamic Calls to Action (i.e. interactive widgets that are displayed on broadcaster's stream), although more functionality may be added in the future.

# Usage

To start working with the **Advocate SDK**, load the client using:

```python-console
>>> from adv.client import AdvClient
>>> client = AdvClient('my-super-secret-api-key')
```

**Note**: If you don't have an API key, please reach out to use at [info@adv.gg](mailto:info@adv.gg) and tell us about your needs.

## Create a New Dynamic Call to Action

To create a new DCTA (Dynamic Call to Action) -- our interactive, on-screen applications -- you first need to fetch your currently active campaigns:

```python-console
>>> my_campaigns = client.get_campaigns()
>>> my_campaigns
[<Campaign: My Hearthstone Campaign>, <Campaign: Going to E3>]
```

you can create a new DCTA on a campaign using the `create_dcta` method:

```python-console
>>> my_campaigns = client.get_campaigns()
>>> campaign = my_campaigns[0]
>>> campaign.create_dcta(name='Lower Thirds DCTA')
<DCTA: Lower Thirds DCTA>
```

Possible kwargs are:

- **name** (required): A short, human-readable name describing your DCTA
- **global_styes**: A python dictionary of of dictionaries, describing CSS styles that will be added to the browersource's `<head>` tag. For example:

    ```python
    {
        '.my-class': {
            'position': 'absolute',
            'top': '10px'
            ...
        },
        '#my-id: {
            ...
        }
        ...
    }
    ```

    These can be updated later, and do not have to be defined when you initial create the DCTA.


## Fetch Existing DCTAs

To get all of your current DCTAS, you can use the `get_dctas` method:

```python-console
>>> client.get_dctas()
[<DCTA: Triva Night App>, <DCTA: Lower Thirds DCTA>]
```

## Render a DCTA

Calling the `render` function on a dcta will re-render the DCTA for all currently streaming broadcasters that are displaying this DCTA on their stream.  Call this after updating your widgets to make sure the newly updated widgets are rendered properly:

```python-console
>>> dctas = client.get_dctas()
>>> my_dcta = dctas[0]
>>> my_dcta.render()
```

## Add a widget to a DCTA

DCTAs are built out of a combination of `Widget` objects that correspond to certain HTML elements.  They currently include:

- **Text Widget**: For inserting easily-updatable text into your DCTA. Creates a `<p>` tag.
- **Image Widget**: Adds images to your DCTA.  Creates a `<img>` tag.
- **Group Widget**: For grouping multiple elements together (e.g. for applying CSS animations or position to a group of elmenets).  Creates a `<div>` tag.
- **Video Widget**: Coming soon.

to create a new text widget, use the `add_text_widget` method on any DCTA object:

```python-console
>>> my_dcta.add_text_widget(name='Lower Thirds Headline Text', text='Breaking News!')
<Widget (text): Lower Thirds Headline Text>
```

Once a widget has been added to a DCTA, you'll be able to see it using the `widgets` field on the DCTA:

```python-console
>>> my_dcta.widgets
[<Widget (text): Lower Thirds Headline Text>]
```

The following kwargs are shared on all widget types:

- **name** (required): A short, human-readable name describing your Widget
- **styles**: A dictionary of CSS styles that will be applied, inline, to your widget
- **attributes**: A dictionary of addition HTML attributs (e.g. `class`) that will be added to your Widget
- **broadcasters**: A list of broadcaster usernames to add to this widget. If a widget has **no** broadcasters, it will be visible to **all** broadcasters.  If the widget has broadcasters, it will only be shown to those broadcasters.  This allows specific parts of a widget to be targeted to specific broadcasters (e.g. unique, broadcasters specific text for each broadcaster).
- **parent**: ID of a Group widget that is the parent of the current widget. Can be None if the widget has no parent (i.e. is a root element)

The following kwargs are on particular widgets:

- **Text Widget**:
    - **text** (required): The actual text content to be displayed
- **Image Widget**:
    - **src** (required): URL to the image to show.
- **Video Widget**:
    - Coming Soon

## Update a Widget

Use the `update` method on any widget to update any of the above properties on the widget:

```python-console
>>> my_widget = my_dcta.widgets[0]
>>> my_widget
<Widget (text): Lower Thirds Headline Text>
>>> my_widget.text
'Breaking News!'
>>> my_widget.update(text='Old News!')
<Widget (text): Lower Thirds Headline Text>
>>> my_widget.text
'Old News!'
```

**Note**: This will update the widget data on the server, but it will **not** cause the DCTA to re-render and display the new information.  This is because rendering can be computationally expensive, and you may want to update multiple widgets before you render.  To force a re-render of the DCTA after an update, you can add the `force_render` kwarg:

```python-console
>>> my_widget.update(text='Look Ma, Immediate Update!', force_render=True)
```

This is the equivalent of calling:

```python-console
>>> my_widget.update(text='Look Ma, Manual Render!')
>>> my_widget.dcta.render()
```
