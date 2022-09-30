// Display table data based on what is selected in the Filter section
const displayTableData = () => {
    $('#dashboard-filter-form').submit(function(e) {
        e.preventDefault();
        
        // Display type of table data (commands created or saved by user)
        const dataShown = $('#display-table-data').val();
        let dataElement = null;
        if (dataShown === "1") {
            $('.commands-created-data').show();
            $('.commands-saved-data').hide();
            dataElement = $('.commands-created-data')
        } else if (dataShown === "2") {
            $('.commands-created-data').hide();
            $('.commands-saved-data').show();
            dataElement = $('.commands-saved-data')
        }

        // Display commands that have selected stacks
        const stacksChosen = $('#display-stacks').val();
        // console.log(stacksChosen);
        const dataRows = dataElement.children();
        if (stacksChosen.length > 0) {
            for (let i = 0; i < dataRows.length; i++) {
                const dataRow = dataRows.eq(i)
                const rowStacks = dataRow.children().eq(1).text().split(", ");
                let founded = false;
                for (let i = 0; i < rowStacks.length; i++) {
                    const stack = rowStacks[i].toLowerCase().replace(/\s+/g, '');
                    if (stacksChosen.includes(stack)){
                        founded = true
                        break;
                    }
                }
                if (!founded) {
                    dataRow.hide();
                } else {
                    dataRow.show();
                }
            }
        } else {
            dataRows.show();
        }
        
    })
}

const init = () => {
    // Hide other table datas and display commands created by the user by default
    $('.commands-saved-data').hide();

    displayTableData();
}

init();