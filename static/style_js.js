window.onload = async () => {
    // Charger les infos globales
    const res = await fetch('/api/moyenne');
    const data = await res.json();

    document.getElementById('global-info').innerHTML = `
        <h2>📊 Données globales</h2>
        <p><strong>Moyenne des températures :</strong> ${data.average} °C</p>
        <p><strong>Nombre de jours mesurés :</strong> ${data.days}</p>
    `;
};
