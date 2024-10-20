document.addEventListener('DOMContentLoaded', function () {
    const citySelect = document.getElementById('city');
    const regionSelect = document.getElementById('region');
    const districtSelect = document.getElementById('district');
    const typeBreadSelect = document.getElementById('typeBread');

    get_cities();
    get_typeBread();

    async function get_cities() {
        const response = await fetch('/api/cities');
        const data = await response.json();
        data.forEach(city => {
            let option = document.createElement('option');
            option.value = city;
            option.textContent = city;           
            citySelect.appendChild(option);
        })        
    };

    async function get_typeBread() {
        const response = await fetch('/api/typeBread');
        const data = await response.json();
        data.forEach(typeBread => {
            let option = document.createElement('option');
            option.value = typeBread;
            option.textContent = typeBread;           
            typeBreadSelect.appendChild(option);
        })        
    };
    
    citySelect.addEventListener('change', function () {
        const city = this.value;
        regionSelect.innerHTML = '<option value="">منطقه را انتخاب کنید ...</option>';
        
        if (city) {
            fetch(`/api/regions/${city}`)
                .then(response => response.json())
                .then(data => {
                    data.forEach(region => {
                        let option = document.createElement('option');
                        option.value = region;
                        option.textContent = region;
                        regionSelect.appendChild(option);
                    });
                });
        }
    });

    regionSelect.addEventListener('click', function () {
        const region = this.value;
        const city = citySelect.value;
        districtSelect.innerHTML = '<option value="">ناحیه را انتخاب کنید ...</option>';

        if (region) {
            fetch(`/api/districts/${region}/${city}`)
                .then(response => response.json())
                .then(data => {
                    data.forEach(district => {
                        let option = document.createElement('option');
                        option.value = district;
                        option.textContent = district;
                        districtSelect.appendChild(option);
                    });
                });
        }
    });
});