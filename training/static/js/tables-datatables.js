
// Tables-DataTables.js
// ====================================================================
// This file should not be included in your project.
// This is just a sample how to initialize plugins or components.
//
// - ThemeOn.net -



$(document).on('nifty.ready', function() {


    // DATA TABLES
    // =================================================================
    // Require Data Tables
    // -----------------------------------------------------------------
    // http://www.datatables.net/
    // =================================================================

    $.fn.DataTable.ext.pager.numbers_length = 5;


    // Basic Data Tables with responsive plugin
    // -----------------------------------------------------------------
    $('#demo-dt-basic').dataTable( {
        "responsive": true,
        "language": {
            "sProcessing":     "Procesando...",
        	"sLengthMenu":     "Mostrar _MENU_ registros",
        	"sZeroRecords":    "No se encontraron resultados",
        	"sEmptyTable":     "Ningún dato disponible en esta tabla",
        	"sInfo":           "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
        	"sInfoEmpty":      "Mostrando registros del 0 al 0 de un total de 0 registros",
        	"sInfoFiltered":   "(filtrado de un total de _MAX_ registros)",
        	"sInfoPostFix":    "",
        	"sSearch":         "Buscar:",
        	"sUrl":            "",
        	"sInfoThousands":  ",",
        	"sLoadingRecords": "Cargando...",
            "paginate": {
              "previous": '<i class="demo-psi-arrow-left"></i> Anterior',
              "next": 'Siguiente <i class="demo-psi-arrow-right"></i>'
            }
        }
    } );

    //#2
    $('#demo-dt-basic-2').dataTable( {
        "responsive": true,
        "language": {
            "sProcessing":     "Procesando...",
        	"sLengthMenu":     "Mostrar _MENU_ registros",
        	"sZeroRecords":    "No se encontraron resultados",
        	"sEmptyTable":     "Ningún dato disponible en esta tabla",
        	"sInfo":           "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
        	"sInfoEmpty":      "Mostrando registros del 0 al 0 de un total de 0 registros",
        	"sInfoFiltered":   "(filtrado de un total de _MAX_ registros)",
        	"sInfoPostFix":    "",
        	"sSearch":         "Buscar:",
        	"sUrl":            "",
        	"sInfoThousands":  ",",
        	"sLoadingRecords": "Cargando...",
            "paginate": {
              "previous": '<i class="demo-psi-arrow-left"></i> Anterior',
              "next": 'Siguiente <i class="demo-psi-arrow-right"></i>'
            }
        }
    } );





    // Row selection (single row)
    // -----------------------------------------------------------------
    var rowSelection = $('#demo-dt-selection').DataTable({
        "responsive": true,
        "language": {
            "paginate": {
              "previous": '<i class="demo-psi-arrow-left"></i>',
              "next": '<i class="demo-psi-arrow-right"></i>'
            }
        }
    });

    $('#demo-dt-selection').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            rowSelection.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    } );






    // Row selection and deletion (multiple rows)
    // -----------------------------------------------------------------
    var rowDeletion = $('#demo-dt-delete').DataTable({
        "responsive": true,
        "language": {
            "paginate": {
              "previous": '<i class="demo-psi-arrow-left"></i>',
              "next": '<i class="demo-psi-arrow-right"></i>'
            }
        },
        "dom": '<"toolbar">frtip'
    });
    $('#demo-custom-toolbar').appendTo($("div.toolbar"));

    $('#demo-dt-delete tbody').on( 'click', 'tr', function () {
        $(this).toggleClass('selected');
    } );

    $('#demo-dt-delete-btn').click( function () {
        rowDeletion.rows('.selected').remove().draw( false );
    } );






    // Add Row
    // -----------------------------------------------------------------
    var t = $('#demo-dt-addrow').DataTable({
        "responsive": true,
        "language": {
            "paginate": {
              "previous": '<i class="demo-psi-arrow-left"></i>',
              "next": '<i class="demo-psi-arrow-right"></i>'
            }
        },
        "dom": '<"newtoolbar">frtip'
    });
    $('#demo-custom-toolbar2').appendTo($("div.newtoolbar"));

    var randomInt = function(min,max){
        return Math.floor(Math.random()*(max-min+1)+min);
    }
    $('#demo-dt-addrow-btn').on( 'click', function () {
        t.row.add( [
            'Adam Doe',
            'New Row',
            'New Row',
            randomInt(1,100),
            '2015/10/15',
            '$' + randomInt(1,100) +',000'
        ] ).draw();
    } );


});
