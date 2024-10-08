from django import forms


class DaisyFormHelper:
    
    def attrs(self, field_name, attrs):
        """
        Update field attributes
        """
        attrs.pop('class', '')
        self.form.fields[field_name].widget.attrs.update(attrs)
         
    
    
    def add_class(self, field_name, css_class):
        """
        Add a class to a field, leaving other classes intact
        """
        classes = self.form.fields[field_name].widget.attrs.get('class', '')
        if len(classes) > 0:
            classes += ' '
            
        apply_classes = classes + css_class
        self.form.fields[field_name].widget.attrs.update({'class': apply_classes})
        
          
    def __init__(self, form):
        self.widget_attrs = {}
        self.form = form
        
        for field_name, x in form.fields.items():            
            
            # apply defaults
            
            if isinstance(x.widget,forms.widgets.Input): 
                x.widget.attrs.update({
                    'class': 'input input-bordered'
                })
            elif  isinstance(x.widget, forms.widgets.ChoiceWidget):
                x.widget.attrs.update({
                    'class': 'select select-bordered'
                })
            elif isinstance(x.widget, forms.widgets.Textarea):
                x.widget.attrs.update({
                        'class': 'textarea textarea-bordered'
                    })
             