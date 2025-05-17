/** @odoo-module **/

import { HeaderCvs } from "./utils";


export const downloadCvs = () => {
    const fixtures = document.querySelectorAll(".rounds-fixture");
    const rows = [];

    if (fixtures.length === 0) {
        alert("No hay datos para exportar.");
        return;
    }

    // Encabezado CSV
    rows.push(HeaderCvs);

    fixtures.forEach((fixture) => {
        try {
            const liga = fixture.querySelector("h6")?.textContent.trim() || "N/A";
            const fecha = fixture.querySelector(".fa-calendar-alt")?.parentElement?.textContent.trim() || "N/A";

            const local = fixture.querySelectorAll("h5")[0]?.textContent.trim() || "N/A";
            const ptsLocal = fixture.querySelectorAll("small")[0]?.textContent.match(/Pts: (\d+)/)?.[1] || "N/A";

            const visitante = fixture.querySelectorAll("h5")[1]?.textContent.trim() || "N/A";
            const ptsVisitante = fixture.querySelectorAll("small")[1]?.textContent.match(/Pts: (\d+)/)?.[1] || "N/A";

            const prediccion = fixture.querySelector(".fa-comment")?.nextElementSibling?.textContent.trim() || "N/A";
            const ganador = fixture.querySelector(".fa-trophy.text-success")?.nextElementSibling?.textContent.trim() || "N/A";

            rows.push([liga, fecha, local, ptsLocal, visitante, ptsVisitante, prediccion, ganador]);

        } catch (error) {
            console.warn("Error extrayendo datos de un fixture:", error);
        }
    });

    // Si no hay filas válidas (sólo encabezado), alertar
    if (rows.length <= 1) {
        alert("No hay partidos válidos para exportar.");
        return;
    }

    // Convertir a CSV
    const csv = rows.map((row) => row.join(",")).join("\n");
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });

    // Descargar archivo
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "fixtures.csv";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}