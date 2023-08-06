import createAsyncAction from '../../../createAsyncAction';
import ApiService from '../../services/api.service';
import HttpService from '../../services/http.service';

export const FETCH_EXAMPLE = '@@{{ component_name }}/FETCH_EXAMPLE';

export const FetchExampleAction = createAsyncAction(FETCH_EXAMPLE, () => {
  const options = ApiService.getOptions('fetchExample');
  return HttpService.fetch(options);
});

