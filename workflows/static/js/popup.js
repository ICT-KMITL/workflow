var renderForm = function(formData) {
    $('.fb-editor').empty();
     var templates = {
    starRating: function(fieldData) {
      return {
        field: '<span id="'+fieldData.name+'">',
        onRender: function() {
          $(document.getElementById(fieldData.name)).rateYo({rating: 3.6});
        }
      };
    }
  };


    // Disable options
    var options = {
        onSave: function (e, formData) {
            console.log(e);
            window.e = e;
            console.log(formData);
            console.log(window.xml);

            var xmlDocument = $.parseXML(window.xml);
            var xml = $(xmlDocument);

            var tasks = xml.find("task");
            tasks.each(function (task_i) {
                if (tasks[task_i].id == window.currentId) {


                    var is_form = 0;
                    for(var i = 0; i<tasks[task_i].childNodes.length; i++){
                        if (tasks[task_i].childNodes[i].tagName == 'documentation' && is_form==0){
                            is_form = 1
                             $(tasks[task_i].childNodes[i]).replaceWith("<documentation>" + formData + "</documentation>");

                            //isform = 1;
                            console.log('------------append');
                            //$(tasks[task_i].childNodes[i]).append(formData)
                        }
                    }

                    //console.log("doc", $(tasks[task_i]).find("documentation").text())
                    //if ($(tasks[task_i]).find("documentation").text() == "")

                    if(is_form == 0) {
                        console.log('=------------create new');
                        console.log(tasks[task_i]);
                        $(tasks[task_i]).append("<documentation>" + formData + "</documentation>")
                    }


                }
            });

            var newXml = (new XMLSerializer()).serializeToString(xmlDocument)


            window.xml = newXml;

            console.log(window.xml);

            //console.info('diagram saved');
            //console.info(xml);
            //$.ajax({
            //url: "modeler/",
            //type: "POST",
            //data: {userXml: window.xml}
            //}).done(function (data) {
            //location.href = "/workflows/";

            // });


            window.x = xml
        },


        disableFields: [
            //'autocomplete',
            // 'button',
            //'checkbox',
            'checkbox-group',
            // 'date',
            //'file',
            //'header',
            //'hidden',
            //'paragraph',
            'number',
            //'radio-group',
            //'select',
            // 'text',
            // 'textarea'
        ],
        editOnAdd: true,
        notify: {
            error: function (message) {
                return console.error(message);
            },
            success: function (message) {
                return console.log(message);
            },
            warning: function (message) {
                return console.warn(message);
            }
        },
        messages: {
            text: 'Text Box',
        },
        sortableControls: true
    };

    if(formData != null) {
        options["dataType"] = 'json';
        options["formData"] = formData;
    }


    // Call options
    $('.fb-editor').formBuilder(options);
    document.querySelector('.form-builder-save').click(function () {
        var allEditorValues = $('.fb-editor').map(function () {
            return $(this).data('formBuilder').formData
        });
        console.log(allEditorValues);
    });

}

console.log("Hi", renderForm)

window.renderForm = renderForm;

