/*! SVG Türkiye Haritası | MIT Lisans | dnomak.com */

function svgturkiyeharitasi() {
    const element = document.querySelector('#svg-turkiye-haritasi');
    const info = document.querySelector('#il-isimleri');

    element.addEventListener(
        'mouseover',
        function (event) {
            debugger;
            console.log(event.target.parentNode.id)
            if (event.target.tagName === 'path' && event.target.parentNode.id !== 'guney-kibris') {
                info.innerHTML = [].join('');
            }
        }
    );

    element.addEventListener(
        'mousemove',
        function (event) {
            info.style.top = event.pageY + 25 + 'px';
            info.style.left = event.pageX + 'px';
        }
    );

    element.addEventListener(
        'mouseout',
        function (event) {
            info.innerHTML = '';
        }
    );

    element.addEventListener(
        'click',
        function (event) {
            if (event.target.tagName === 'path') {
                const parent = event.target.parentNode;
                const id = parent.getAttribute('id');

                if (
                    id === 'guney-kibris'
                ) {
                    return;
                }

                window.location.href = (
                    '#'
                    + id
                    + '-'
                    + parent.getAttribute('data-plakakodu')
                );
            }
        }
    );
}
