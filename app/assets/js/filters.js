document.addEventListener('DOMContentLoaded', function () {
    const citySelect = document.getElementById('city');
    const regionSelect = document.getElementById('region');
    const districtSelect = document.getElementById('district');
    const typeBreadSelect = document.getElementById('typeBread');
    const typeFlourSelect = document.getElementById('typeFlour');
    const secondFuelSelect = document.getElementById('secondFuel');

    get_cities();
    get_typeBread();
    get_typeFlour();
    get_secondFuel();


    async function get_cities() {
        const response = await fetch('/api/dashboard/cities');
        const data = await response.json();
        data.forEach(city => {
            let option = document.createElement('option');
            option.value = city;
            option.textContent = city;           
            citySelect.appendChild(option);
        })        
    };

    citySelect.addEventListener('change', function () {
        const city = this.value;
        regionSelect.innerHTML = '<option value="">منطقه را انتخاب کنید ...</option>';
        if (city) {
            fetch(`/api/dashboard/regions/${city}`)
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
            fetch(`/api/dashboard/districts/${city}/${region}`)
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

    async function get_typeBread() {
        const response = await fetch('/api/dashboard/type_bread');
        const data = await response.json();
        data.forEach(typeBread => {
            let option = document.createElement('option');
            option.value = typeBread;
            option.textContent = typeBread;           
            typeBreadSelect.appendChild(option);
        })        
    };

    async function get_typeFlour() {
        const response = await fetch('/api/dashboard/type_flour');
        const data = await response.json();
        data.forEach(typeFlour => {
            let option = document.createElement('option');
            option.value = typeFlour;
            option.textContent = typeFlour;           
            typeFlourSelect.appendChild(option);
        })        
    };

    async function get_secondFuel() {
        const response = await fetch('/api/dashboard/second_fuel');
        const data = await response.json();
        data.forEach(secondFuel => {
            let option = document.createElement('option');
            option.value = secondFuel;
            option.textContent = secondFuel;           
            secondFuelSelect.appendChild(option);
        })        
    };
    
});