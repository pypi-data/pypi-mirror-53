# Template Generator

This project is intended to unify boilerplate code between team members and make the setup process for starting a new component shorter and less tedious.

### Installation
```bash
python -m pip install TemplateCreator
```

### Usage
```bash
python -m TemplateCreator --template shared-component --folder-name my-example
```  
or use the short syntax
```bash
python -m TemplateCreator -t shared-component -n my-example
```
Components with name constructed of multiple words should be separated by '-' this will result in camel cased class name (MyExampleComponent)

### Template options
--template shared-component

--template class_component

--template function_component 

--template state

#### shared-component
creates 4 files:
* my-component.component.jsx
* my-component.styles.js
* my-component.readme.md
* my-component.test.jsx

#### class-component / function-component
creates 2 files:
* my-component.component.jsx
* my-component.styles.scss

#### state
creates 3 files:
* my-state.reducer.js
* my-state.state.js
* my-state.actions.js

### Add A New Template
1. Add a new template file (follow jinja2 convention) to templates folder (for example: my-new-template.jsx) 

2. In template_options.py add TemplateInfo(name='my-new-template', file_name=f'{folder_name}.custom.jsx'). 
The name attribute should be the same as the template name (without the extension)

3. Update template_options.py get_dictionary method with a key (passed in as --template parameter) 
and a value of list of TemplateInfo to create  
