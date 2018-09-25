Date.prototype.asMySQL = function() {
    let res = "" + this.getFullYear() + "-";
    if( this.getMonth() < 9 ) {
        res += "0";
    }
    res += ( this.getMonth() + 1 ) + "-";
    if( this.getDate() < 10 ) {
        res += "0";
    }
    res += this.getDate();
    return res;
}
Date.prototype.asMx = function() {
    let res = "";
    if( this.getDate() < 10 ) {
        res += "0";
    }
    res += this.getDate() + "/";
    if( this.getMonth() < 9 ) {
        res += "0";
    }
    res += ( this.getMonth() + 1 ) + "/" + this.getFullYear();
    return res;
}

class clsApp {
    inputFileOpen(  ) {
        let iframe_url = uploader.url + "?";
        if( uploader.site ) { iframe_url += "site=" + uploader.site + "&"; }
        if( uploader.key ) { iframe_url += "key=" + uploader.key + "&"; }
        if( uploader.onresponse ) { iframe_url += "onresponse=" + uploader.onresponse + "&"; }
        if( uploader.type ) { iframe_url += "type=" + uploader.type + "&"; }
        if( uploader.excecute ) { iframe_url += "excecute=" + uploader.excecute + "&"; }
        if( uploader.token ) { iframe_url += "token=" + uploader.token + "&"; }
        if( uploader.message ) { iframe_url += "message=" + uploader.message + "&"; }

        let iframe = $( `<iframe style="width: 100%;" src="${iframe_url}" id="uploader-frame" frameborder="0"></iframe>` );

        this.openPanel( ' ', "Cargar Archivo" );
        $( "#modal-panel-message .modal-body").html( iframe[0].outerHTML );
    }
    checkInputIn( idcontainer ) {
        $( '#' + idcontainer + ' input[type="checkbox"]' ).attr( 'checked', true );
    }
    uncheckInputIn( idcontainer ) {
        $( '#' + idcontainer + ' input[type="checkbox"]' ).attr( 'checked', false );
    }
    openPanel( body, title, close = true, footer = null ) {
        let template = Handlebars.compile( $( "#modal-panel-message-template" ).html() );
        let html = template( { "title" : title, "body" : body, "footer" : footer, "close" : close } );
        $( "#modal-panel-message" ).remove();
        $( document.body ).append( $( html ) );
        $( "#modal-panel-message" ).modal();
    }
}

class clsProd {
    showChargeForm( idcte, clave, nombre ) {
        let template = Handlebars.compile( $( "#aplicar-cargo-template" ).html() );
        let context = { cte : idcte, today : ( new Date() ).asMySQL(), prods : productos };
        let html = template( context );
        App.openPanel( html, `Aplicar Venta ${ clave || nombre ? 'a' : '' } ${ clave ? ( clave + ( nombre ? ' - ' : '' ) ) : '' } ${ nombre ? nombre : '' }` );
        if( req_ui ) {
            $( `input[type="date"]` ).datepicker( {
                changeMonth: true,
                changeYear: true,
                dateFormat : 'yy-mm-dd'  
            } );
        }
    }
    setChargeInfo() {
        let idprod = $( "#product" ).val();
        let prod = null;
        for( let idx = 0; idx < productos.length; idx++ ) {
            if( productos[ idx ].pk == idprod ) {
                prod = productos[ idx ];
                break;
            }
        }
        if( prod ) {
            $( "#monto_cargo" ).attr( 'value', prod.precio );    
            $( "#concepto_cargo" ).attr( 'value', prod.nombre );
        }
    }
    showPaymentForm( idcte, clave, nombre ) {
        $.getJSON( BASE_URL + '/movimientos/ventas/' + idcte + '/', ( movs ) => {
            let cont = 0;
            for( let idx in movs.charges ) {
                if( parseFloat( movs.charges[ idx ].saldo ) > 0.0 ) {
                    cont++;
                    break;
                }
            }
            if( 0 == movs.charges.length || ! cont ) {
                App.openPanel(  "El cliente no tiene cargos con saldo", "Mensaje de Sistema" );
                return false;
            }
            let template = Handlebars.compile( $( "#aplicar-abono-template").html() );
            let context = { cte : idcte, today : ( new Date() ).asMySQL() };
            let html = template( context );
            App.openPanel( html, `Aplicar Pago ${ clave || nombre ? 'a' : '' } ${ clave ? ( clave + ( nombre ? ' - ' : '' ) ) : '' } ${ nombre ? nombre : '' }` );
            $( "#cargo option" ).remove();
            $( "#concepto_abono" ).attr( 'value', '' );
            $( "#monto_abono" ).attr( 'value', '' );
            $( "#cargo" ).append( $( `<option></option>` ) );
            for( let idx in movs.charges ) {
                if( parseFloat( movs.charges[ idx ].saldo ) > 0.0 )
                    $( "#cargo" ).append( $( `<option value="${movs.charges[ idx ].id}" data-saldo="${movs.charges[ idx ].saldo}">${movs.charges[ idx ].cargo}</option>` ) );
            }
            $( "#no_de_pago" ).attr( 'value', movs.no_abono );
            if( req_ui ) {
                $( `input[type="date"]` ).datepicker( {
                    changeMonth: true,
                    changeYear: true,
                    dateFormat : 'yy-mm-dd'  
                } );
            }
        } );
    }
    setPaymentInfo() {
        let concepto = "Pago de ";
        let idcargo = $( "#cargo" ).val();
        let cargo = $( `#cargo option[value="${idcargo}"]` ).text().trim();
        $( "#concepto_abono" ).attr( 'value', concepto + cargo );
        $( "#monto_abono" ).attr( 'value', $( `#cargo option[value="${idcargo}"]` ).attr( 'data-saldo' ) );
    }
    verifyPaymentInfo() {
        $( '#aplicar-abono input[name="cte"]' ).attr( 'value', $( "#client" ).val() )
        let idcargo = $( "#cargo" ).val();
        if( "" == idcargo ) {
            alert( "Debe seleccionar un cargo para aplicar el abono" );
            $( "#cargo" ).focus();
            return false;
        }
        let saldo = parseFloat( $( `#cargo option[value="${idcargo}"]` ).attr( 'data-saldo' ) )
        let monto = parseFloat( $( "#monto_abono" ).val() )
        if( monto > saldo ) {
            alert( `El saldo del cargo seleccionado es de ${saldo}, el monto no debe ser mayor.` );
            $( "#monto_abono" ).focus();
            return false;
        }
        return true;
    }
    sumTotalHL() {
        let suma = 0.0;
        $( `#data-tbl input[type="checkbox"]` ).each( function(){ 
            if( this.checked ) {
                suma+= parseFloat( $( this ).attr( 'data-monto' ) ); 
            }
        } );
        $( "#total" ).html( suma );
    }
    showChargePaymentFormEdit( idcte, pk, type, fecha, monto, concepto ) {
        let template = Handlebars.compile( $( "#editar-venta-pago-template").html() );
        let context = { idcte, pk, type, fecha, monto, concepto };
        let html = template( context );
        App.openPanel( html, "Actualizar " + type );
        if( req_ui ) {
            $( `input[type="date"]` ).datepicker( {
                changeMonth: true,
                changeYear: true,
                dateFormat : 'yy-mm-dd'  
            } );
        }
    }
}

class clsCte {
    showNotas( idcte, clave, nombre ) {
        $.getJSON( BASE_URL + '/clientes/notas/' + idcte + '/', ( notas ) => {
            let template = Handlebars.compile( $( "#notas-cte-template" ).html() );
            let context = { idcte, idusrvendedor : $( "#idusrvendedor").val(), notas };
            let html = template( context );
            App.openPanel( html, `${clave} - ${nombre}` );
        } );
    }
}

let App = new clsApp();
let Prod = new clsProd();
let Cte = new clsCte();

$( document ).ready( () => { $('[data-toggle="tooltip"]').tooltip(); } );