
// Form-Validation.js
// ====================================================================
// This file should not be included in your project.
// This is just a sample how to initialize plugins or components.
//
// - ThemeOn.net -


$(document).on('nifty.ready', function() {


    // FORM VALIDATION
    // =================================================================
    // Require Bootstrap Validator
    // http://bootstrapvalidator.com/
    // =================================================================


    // FORM VALIDATION FEEDBACK ICONS
    // =================================================================
    var faIcon = {
        valid: 'fa fa-check-circle fa-lg text-success',
        invalid: 'fa fa-times-circle fa-lg',
        validating: 'fa fa-refresh'
    }



    // FORM VALIDATION ON TABS
    // =================================================================
    $('#demo-bv-bsc-tabs').bootstrapValidator({
        excluded: [':disabled'],
        feedbackIcons: faIcon,
        fields: {
        fullName: {
            validators: {
                notEmpty: {
                    message: 'Se requiere el nombre completo'
                }
            }
        },
        company: {
            validators: {
                notEmpty: {
                    message: 'El nombre de la empresa es obligatorio.'
                }
            }
        },
        memberType: {
            validators: {
                notEmpty: {
                    message: 'Elija el tipo de membresía que mejor se adapte a sus necesidades'
                }
            }
        },
        address: {
            validators: {
                notEmpty: {
                    message: 'La direccion es requerida'
                }
            }
        },
        city: {
            validators: {
                notEmpty: {
                    message: 'La ciudad es obligatoria'
                }
            }
        },
        country: {
            validators: {
                notEmpty: {
                    message: 'El pais es obligatorio'
                }
            }
        }
        }
    }).on('status.field.bv', function(e, data) {
        var $form     = $(e.target),
        validator = data.bv,
        $tabPane  = data.element.parents('.tab-pane'),
        tabId     = $tabPane.attr('id');

        if (tabId) {
        var $icon = $('a[href="#' + tabId + '"][data-toggle="tab"]').parent().find('i');

        // Add custom class to tab containing the field
        if (data.status == validator.STATUS_INVALID) {
            $icon.removeClass(faIcon.valid).addClass(faIcon.invalid);
        } else if (data.status == validator.STATUS_VALID) {
            var isValidTab = validator.isValidContainer($tabPane);
            $icon.removeClass(faIcon.valid).addClass(isValidTab ? faIcon.valid : faIcon.invalid);
        }
        }
    });


    // FORM VALIDATION ON ACCORDION
    // =================================================================
    $('#demo-bv-accordion').bootstrapValidator({
        message: 'Este valor no es valido',
        excluded: ':disabled',
        feedbackIcons: faIcon,
        fields: {
        firstName: {
            validators: {
                notEmpty: {
                    message: 'El primer nombre es obligatorio y no puede estar vacío'
                },
                regexp: {
                    regexp: /^[A-Z\s]+$/i,
                    message: 'El primer nombre solo puede consistir en caracteres alfabéticos y espacios'
                }
            }
        },
        lastName: {
            validators: {
                notEmpty: {
                    message: 'El apellido es obligatorio y no puede estar vacío.'
                },
                regexp: {
                    regexp: /^[A-Z\s]+$/i,
                    message: 'El apellido solo puede consistir en caracteres alfabéticos y espacios'
                }
            }
        },
        username: {
            message: 'El nombre de usuario no es válido',
            validators: {
                notEmpty: {
                    message: 'El nombre de usuario es obligatorio y no puede estar vacío'
                },
                stringLength: {
                    min: 4,
                    max: 30,
                    message: 'El nombre de usuario debe tener más de 4 y menos de 30 caracteres.'
                },
                regexp: {
                    regexp: /^[a-zA-Z0-9_\.]+$/,
                    message: 'El nombre de usuario solo puede constar de letras, números, puntos y guiones bajos.'
                },
                different: {
                    field: 'password',
                    message: 'El nombre de usuario y la contraseña no pueden ser iguales entre sí.'
                }
            }
        },
        email: {
            validators: {
                notEmpty: {
                    message: 'La dirección de correo electrónico es obligatoria y no puede estar vacía.'
                },
                emailAddress: {
                    message: 'La entrada no es una dirección de correo electrónico válida'
                }
            }
        },
        password: {
            validators: {
                notEmpty: {
                    message: 'La contraseña es obligatoria y no puede estar vacía.'
                },
                different: {
                    field: 'username',
                    message: 'La contraseña no puede ser la misma que el nombre de usuario'
                }
            }
        },
        memberType: {
            validators: {
                notEmpty: {
                    message: 'El género es obligatorio.'
                }
            }
        },
        bio:{
            validators: {
                notEmpty: {
                    message: 'La biografía es obligatoria y no puede estar vacía.'
                },
            }
        },
        phoneNumber: {
            validators: {
                notEmpty: {
                    message: 'El número de teléfono es obligatorio y no puede estar vacío.'
                },
                digits: {
                    message: 'El valor solo puede contener dígitos'
                }
            }
        },
        city:{
            validators: {
                notEmpty: {
                    message: 'La ciudad es obligatoria y no puede estar vacía.'
                },
            }
        }
        }
    }).on('status.field.bv', function(e, data) {
        var $form = $(e.target),
        validator = data.bv,
        $collapsePane = data.element.parents('.collapse'),
        colId = $collapsePane.attr('id');

        if (colId) {
        var $anchor = $('a[href="#' + colId + '"][data-toggle="collapse"]');
        var $icon = $anchor.find('i');

        // Add custom class to panel containing the field
        if (data.status == validator.STATUS_INVALID) {
            $anchor.addClass('bv-col-error');
            $icon.removeClass(faIcon.valid).addClass(faIcon.invalid);
        } else if (data.status == validator.STATUS_VALID) {
            var isValidCol = validator.isValidContainer($collapsePane);
            if (isValidCol) {
                $anchor.removeClass('bv-col-error');
            }else{
                $anchor.addClass('bv-col-error');
            }
            $icon.removeClass(faIcon.valid + " " + faIcon.invalid).addClass(isValidCol ? faIcon.valid : faIcon.invalid);
        }
        }
    });


    // FORM VALIDATION CUSTOM ERROR CONTAINER
    // =================================================================
    // Indicate where the error messages are shown.
    // Tooltip, Popover, Custom Container.
    // =================================================================
    $('#demo-bv-errorcnt').bootstrapValidator({
        message: 'Este valor no es valido',
        excluded: [':disabled'],
        feedbackIcons: faIcon,
        fields: {
        name: {
            container: 'tooltip',
            validators: {
                notEmpty: {
                    message: 'El primer nombre es obligatorio y no puede estar vacío'
                },
                regexp: {
                    regexp: /^[A-Z\s]+$/i,
                    message: 'El primer nombre solo puede consistir en caracteres alfabéticos y espacios'
                }
            }
        },
        lastName: {
            validators: {
                notEmpty: {
                    message: 'El apellido es obligatorio y no puede estar vacío.'
                },
                regexp: {
                    regexp: /^[A-Z\s]+$/i,
                    message: 'El apellido solo puede consistir en caracteres alfabéticos y espacios'
                }
            }
        },
        email: {
            container: 'tooltip',
            validators: {
                notEmpty: {
                    message: 'La dirección de correo electrónico es obligatoria y no puede estar vacía.'
                },
                emailAddress: {
                    message: 'La entrada no es una dirección de correo electrónico válida'
                }
            }
        },
        username: {
            container: 'popover',
            message: 'El nombre de usuario no es válido',
            validators: {
                notEmpty: {
                    message: 'El nombre de usuario es obligatorio y no puede estar vacío'
                },
                stringLength: {
                    min: 6,
                    max: 30,
                    message: 'El nombre de usuario debe tener más de 6 y menos de 30 caracteres.'
                },
                regexp: {
                    regexp: /^[a-zA-Z0-9_\.]+$/,
                    message: 'El nombre de usuario solo puede constar de letras, números, puntos y guiones bajos.'
                },
                different: {
                    field: 'password',
                    message: 'El nombre de usuario y la contraseña no pueden ser iguales entre sí.'
                }
            }
            },
        password: {
            container: 'popover',
                validators: {
                    notEmpty: {
                    message: 'La contraseña es obligatoria y no puede estar vacía.'
                    },
                    different: {
                        field: 'username',
                        message: 'La contraseña no puede ser la misma que el nombre de usuario'
                    }
                }
        },
        phoneNumber: {
            container: '#demo-error-container',
            validators: {
                notEmpty: {
                    message: 'El número de teléfono es obligatorio y no puede estar vacío.'
                },
                digits: {
                    message: 'El valor solo puede contener dígitos'
                }
                }
        },
        city:{
            container: '#demo-error-container',
            validators: {
                notEmpty: {
                    message: 'La ciudad es obligatoria y no puede estar vacía.'
                },
            }
        }
        }
    }).on('status.field.bv', function(e, data) {
        var $form     = $(e.target),
        validator = data.bv,
        $tabPane  = data.element.parents('.tab-pane'),
        tabId     = $tabPane.attr('id');

        if (tabId) {
        var $icon = $('a[href="#' + tabId + '"][data-toggle="tab"]').parent().find('i');
        // Add custom class to tab containing the field
        if (data.status == validator.STATUS_INVALID) {
            $icon.removeClass(faIcon.valid).addClass(faIcon.invalid);
        } else if (data.status == validator.STATUS_VALID) {
            var isValidTab = validator.isValidContainer($tabPane);
            $icon.removeClass(faIcon.valid).addClass(isValidTab ? faIcon.valid : faIcon.invalid);
        }
        }
    });


    // FORM VARIOUS VALIDATION
    // =================================================================
    $('#demo-bvd-notempty').bootstrapValidator({
        message: 'Este valor no es valido',
        feedbackIcons: faIcon,
        fields: {
        username: {
            message: 'El nombre de usuario no es válido',
            validators: {
                notEmpty: {
                    message: 'El nombre de usuario es obligatorio.'
                },
                different: {
                    field: 'password',
                    message: 'El nombre de usuario y la contraseña no pueden ser iguales entre sí.'
                }
            }
        },
        acceptTerms: {
            validators: {
                notEmpty: {
                    message: 'Tienes que aceptar los términos y políticas.'
                }
            }
        },
        password: {
            validators: {
                notEmpty: {
                    message: 'La contraseña es obligatoria y no puede estar vacía.'
                },
                identical: {
                    field: 'confirmPassword',
                    message: 'La contraseña y su confirmación no son las mismas.'
                }
            }
        },
        confirmPassword: {
            validators: {
                notEmpty: {
                    message: 'La contraseña de confirmación es obligatoria y no puede estar vacía'
                },
                identical: {
                    field: 'password',
                    message: 'La contraseña y su confirmación no son las mismas.'
                }
            }
        },
        gender: {
            validators: {
                notEmpty: {
                    message: 'El género es obligatorio.'
                }
            }
        },
        'programs[]': {
            validators: {
                choice: {
                    min: 2,
                    max: 4,
                    message: 'Por favor elija 2 - 4 lenguajes de programación en los que es bueno'
                }
            }
        },
        integer: {
            validators: {
                notEmpty: {
                    message: 'El número es requerido y no puede estar vacío'
                },
                integer: {
                    message: 'El valor no es un número.'
                }
            }
        },
        numeric: {
            validators: {
                notEmpty: {
                    message: 'El número es requerido y no puede estar vacío'
                },
                numeric: {
                    message: 'El valor no es un número.'
                }
            }
        },
        greaterthan: {
            validators: {
                notEmpty: {
                    message: 'El número es requerido y no puede estar vacío'
                },
                greaterThan: {
                    inclusive:false,
                    //If true, the input value must be greater than or equal to the comparison one.
                    //If false, the input value must be greater than the comparison one
                    value: 50,
                    message: 'Por favor ingrese un valor mayor a 50'
                }
            }
        },
        lessthan: {
            validators: {
                notEmpty: {
                    message: 'El número es requerido y no puede estar vacío'
                },
                lessThan: {
                    inclusive:false,
                    //If true, the input value must be less than or equal to the comparison one.
                    //If false, the input value must be less than the comparison one
                    value: 25,
                    message: 'Por favor, introduzca un valor inferior a 25'
                }
            }
        },
        range: {
            validators: {
                inclusive:true,
                notEmpty: {
                    message: 'El número es requerido y no puede estar vacío'
                },
                between: {
                    min:1,
                    max:100,
                    message: 'Por favor ingrese un número entre 1 y 100'
                }
            }
        },
        uppercase:{
            validators: {
                notEmpty: {
                    message: 'El titular de la tarjeta es obligatorio y no puede estar vacío.'
                },
                // Since case is a Javascript keyword,
                // you should place it between quotes (like 'case' or "case")
                // to make it work in all browsers
                stringCase: {
                    message: 'El titular de la tarjeta debe estar en mayúsculas.',
                    'case': 'upper'
                }
            }
        },
        email: {
            validators: {
                notEmpty: {
                    message: 'La dirección de correo electrónico es obligatoria y no puede estar vacía.'
                },
                emailAddress: {
                    message: 'La entrada no es una dirección de correo electrónico válida'
                }
            }
        },
        url_path: {
            validators: {
                notEmpty: {
                    message: 'La dirección del sitio web es obligatoria y no puede estar vacía.'
                },
                uri: {
                    allowLocal: false,
                    message: 'La entrada no es una URL válida'
                }
            }
        },
        color: {
            validators: {
                notEmpty: {
                    message: 'El color hexadecimal es obligatorio y no puede estar vacío'
                },
                hexColor: {
                    message: 'La entrada no es un color hexadecimal válido.'
                }
            }
        }
        }
    }).on('success.field.bv', function(e, data) {
        // $(e.target)  --> The field element
        // data.bv      --> The BootstrapValidator instance
        // data.field   --> The field name
        // data.element --> The field element

        var $parent = data.element.parents('.form-group');

        // Remove the has-success class
        $parent.removeClass('has-success');
    });




    // MASKED INPUT
    // =================================================================
    // Require Masked Input
    // http://digitalbush.com/projects/masked-input-plugin/
    // =================================================================


    // Initialize Masked Inputs
    // a - Represents an alpha character (A-Z,a-z)
    // 9 - Represents a numeric character (0-9)
    // * - Represents an alphanumeric character (A-Z,a-z,0-9)
    $('#demo-msk-date').mask('99/99/9999');
    $('#demo-msk-date2').mask('99-99-9999');
    $('#demo-msk-phone').mask('(999) 999-9999');
    $('#demo-msk-phone-ext').mask('(999) 999-9999? x99999');
    $('#demo-msk-taxid').mask('99-9999999');
    $('#demo-msk-ssn').mask('999-99-9999');
    $('#demo-msk-pkey').mask('a*-999-a999');



});
