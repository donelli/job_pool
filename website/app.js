
Vue.component('vue-multiselect', window.VueMultiselect.default)
Vue.use(VueGoogleCharts)

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
      },
      tagsChartData: function() {
         const data =  [
            ["Tag", "Tags count"],
         ]

         for (let i = 0; i < this.filteredTags.length; i++) {
            const tag = this.filteredTags[i];
            
            if (i > 30) {
               break;
            }
            
            data.push([ tag.name, tag.count ]);
            
         }
         
         return data;
      },
      filteredTags: function() {

         const tags = [];
         
         for (const job of this.filteredJobs) {
            
            for (const tag of job.tags) {
               
               let found = false;
               
               for (const tagObj of tags) {
                  
                  if (tagObj.name == tag) {
                     tagObj.count += 1;
                     found = true;
                     break;
                  }
                  
               }

               if (!found) {
                  tags.push({
                     name: tag,
                     count: 1
                  })
               }
               
               // const find = tags.findIndex(tag => tag.name == tag);
               // if (find >= 0) {
               //    tags[find].count += 1;
               // } else {
               //    tags.push({
               //       name: tag,
               //       count: 1
               //    });
               // }
               
            }
            
         }
         
         return tags.sort((a, b) => b.count - a.count);
         
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
         
      },
      clearFilters: function() {
         this.selectedCompanies = [];
         this.textFilter = '';
      }
   }
})
