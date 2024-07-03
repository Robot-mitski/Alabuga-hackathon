export class ModelInputListener {
    #CommunicatorInstance;
    constructor(CommunicatorInstance){
        this.#CommunicatorInstance = CommunicatorInstance;
    }

    async OnSubmit(event){
        event.preventDefault();
        var form = document.getElementById("modelForm");
		var error = document.getElementById("modelError");
        var input = form.modelInput.value;
        var output = document.getElementsByClassName("scroll-table")[0];
        if (input === ""){
            error.innerHTML = "Заполните все поля";
            return false; }
        var resp = await this.#CommunicatorInstance.SendResponse(event.currentTarget.page, {
            "url": input
        }).then((json)=> {return json});
        var resp = JSON.parse(JSON.stringify(resp));
        if (resp.status !== "ok") {
            error.innerHTML = resp.message;
            return false;
        }
        var trs = "";
        var comps = resp.output.companies;
        for (var i = 0; i < comps.length; i++){
            var color = "black";
            if (comps[i].estimate === "POSITIVE") { color = "lime"; }
            else if (comps[i].estimate === "NEGATIVE") { color = "red"; }
            trs += `<tr><th>${comps[i].name}</th><th style="color: ${color}">${comps[i].estimate}</th></tr>`;
        }
        output.innerHTML = `<table>
                    <thead>
                        <tr>
                            <th style="text-align: center;">Организация</th>
                            <th style="text-align: center;">Отношение к ней</th>
                        </tr>
                    </thead>
                </table>	
                <div class="scroll-table-body">
                    <table>
                        <tbody>
                            ${trs}
                        </tbody>
                    </table>
                </div>`;
        return true;
    }
}