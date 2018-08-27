class clsApp {
    inputFileOpen(  ) {
        let iframe_url = uploader.url + "?";
        if( uploader.onresponse ) { iframe_url += "onresponse=" + uploader.onresponse + "&"; }
        if( uploader.excecute ) { iframe_url += "excecute=" + uploader.excecute + "&"; }
        if( uploader.message ) { iframe_url += "message=" + uploader.message + "&"; }

        let iframe = $( `<iframe style="width: 100%;" src="${iframe_url}" id="uploader-frame" frameborder="0"></iframe>` );

        this.openPanel( ' ', "Cargar Archivo" );
        $( "#modal-panel-message .modal-body").html( iframe[0].outerHTML );
    }
    inputLoadedFile( response ) {
        if( "ok" == response.response.toLowerCase().trim() && "" != response.file ) {
            $( "#token" ).attr( 'value', response.file );
            uploader.container.find( 'img' ).remove();
            uploader.container.find( 'label' ).prepend( $( `<img src="${MEDIA_URL + uploader.type + '/' + response.file }" class="rounded-circle float-right" height="40" width="40" />` ) )
            this.closePanel();
            //alert( uploader.type );
        }
    }
    checkInputIn( idcontainer ) {
        $( '#' + idcontainer + ' input[type="checkbox"]' ).attr( 'checked', true );
    }
    uncheckInputIn( idcontainer ) {
        $( '#' + idcontainer + ' input[type="checkbox"]' ).attr( 'checked', false );
    }
    openPanel( body, title, close = true, footer = null ) {
        let template = Handlebars.compile( $( "#modal-panel-message-template" ).html() );
        let context = {title: "Cargar Archivo", body: ' ', close: "yes" };
        let html = template( { "title" : title, "body" : body, "footer" : footer, "close" : close } );
        $( document.body ).append( $( html ) );
        $( "#modal-panel-message" ).modal();
    }
    closePanel() {
        $( "#modal-panel-message .close" ).trigger('click')
    }
}

class clsProd {
    hideFormsMovs() {
        $( "#aplicar-cargo" ).addClass( 'd-none' );
        $( "#aplicar-abono" ).addClass( 'd-none' );
    }
    showChargeForm() {
        this.hideFormsMovs();
        $( "#aplicar-cargo" ).removeClass( 'd-none' );
    }
    setChargeInfo() {
        let idprod = $( "#product" ).val();
        let prod = $( '#product option[value=' + idprod + ']' ).text().split( '/' );
        prod = prod[ prod.length - 1 ].trim();
        $( "#monto_cargo" ).attr( 'value', montos[ idprod ] );
        $( "#concepto_cargo" ).attr( 'value', prod );
    }
    setChargeClientId() {
        $( '#aplicar-cargo input[name="cte"]' ).attr( 'value', $( "#client" ).val() )
        return true;
    }
    showPaymentForm() {
        this.hideFormsMovs()
        let idcte = $( "#client" ).val()
        $.getJSON( BASE_URL + '/movimientos/ventas/' + idcte + '/', ( movs ) => {
            console.log( movs );
            if( 0 == movs.charges.length ) {
                alert( "El cliente no tiene cargos con saldo" );
                return false;
            }
            $( "#cargo option" ).remove();
            $( "#cargo" ).append( $( `<option></option>` ) );
            for( let idx in movs.charges ) {
                if( parseFloat( movs.charges[ idx ].saldo ) > 0.0 )
                $( "#cargo" ).append( $( `<option value="${movs.charges[ idx ].id}" data-saldo="${movs.charges[ idx ].saldo}">${movs.charges[ idx ].cargo}</option>` ) );
            }
            $( "#no_de_pago" ).attr( 'value', movs.no_abono );
            $( "#aplicar-abono" ).removeClass( 'd-none' );
        } );
    }
    setPaymentInfo() {
        let concepto = "Pago de ";
        let idcargo = $( "#cargo" ).val();
        let cargo = $( `#cargo option[value="${idcargo}"]` ).text().trim();
        $( "#concepto_abono" ).attr( 'value', concepto + cargo );
        $( "#monto_abono" ).attr( 'value', $( `#cargo option[value="${idcargo}"]` ).attr( 'data-saldo' ) )
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
    showAcc() {
        location.href = BASE_URL + '/movimientos/' + $( "#client" ).val();
    }
}

window.App = new clsApp();
window.Prod = new clsProd();

$( document ).ready( () => { $('[data-toggle="tooltip"]').tooltip(); } );