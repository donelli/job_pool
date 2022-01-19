
Vue.component('vue-multiselect', window.VueMultiselect.default)


var app = new Vue({
   el: '#app',
   data: {
     isLoading: true,
     jobs: [],
     error: '',
     companies: [],
     selectedCompanies: [],
     textFilter: ''
   },
   mounted: function() {
      this.loadJobs();
   },
   computed: {
      filteredJobs: function() {
         
         const companyNames = this.selectedCompanies.map(company => company.name);
         
         return this.jobs.filter(job => {
            return companyNames.includes(job.company) && (!this.textFilter || job.filters.includes(this.textFilter.toLowerCase()));
         });
      }
   },
   methods: {
      loadJobs: function() {
         
         axios.get('../data/jobs.json')
         .then(resp => {
            
            let companies = [];
            for (const job of resp.data) {
               
               job.filters = job.name.toLowerCase() + ' ' + job.tags.join(" ").toLowerCase();
               
               let found = false;
               
               for (const comp of companies) {
                  if (comp.name == job.company) {
                     found = true;
                     comp.jobs += 1;
                     break;
                  }
               }
               
               if (!found) {
                  companies.push({
                     name: job.company,
                     jobs: 1
                  });
               }
            }

            for (const company of companies) {
               company.nameWithCount = company.name + ' (' + company.jobs + ')';
            }

            this.selectedCompanies = [ ...companies.filter(c => c.name !== 'TOTVS') ];
            
            this.companies = companies;
            this.jobs = resp.data;
         })
         .catch(err => {
            this.error = 'Error loading jobs!';
         })
         .finally(() => {
            this.isLoading = false;            
         });
         
      }
   }
})
