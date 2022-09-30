// Display table data based on what is selected in the Filter section
const displayTableData = () => {
    $('#dashboard-filter-form').submit(function(e) {
        e.preventDefault();
        
        // Display command sets in a certain order
        const sortedBy = $('#sorted-by-select').val();
        $('.commands-created-data').hide();
        $('.commands-saved-data').hide();
    

        // Display type of table data (commands created or saved by user)
        const dataShown = $('#display-table-data').val();
        let dataElement = null;
        if (dataShown === "1") {
            dataElement = $(`.commands-created-data.${sortedBy}`)
            dataElement.show();
            $('#dashboard-table-title').text('Commands created by you');
        } else if (dataShown === "2") {
            dataElement = $(`.commands-saved-data.${sortedBy}`)
            dataElement.show();
            $('#dashboard-table-title').text('Commands saved by you');
        }

        // Display commands that have selected stacks
        const stacksChosen = $('#display-stacks').val();
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
    // Only show commands created by users sorted in last updated by default
    $('.commands-saved-data').hide();
    $('.commands-created-data').hide();
    $('.commands-created-data.sorted-by-last-updated').show();

    displayTableData();
}

init();