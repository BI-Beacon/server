                                                    formdata=data)
        self.assertEqual(400, errcode)
        self.assertEqual("Invalid period", json['message'])
 
    def test_unknown_form_parameter(self):
        def post_packet(lampid, packet):
            pass
        data = {'color': "#00ff00", 'huh': '123'}
        (json, errcode) = V1API(post_packet).handle(id='lamp',
                                                    formdata=data)
        self.assertEqual(400, errcode)
        self.assertEqual("Unknown parameter 'huh'", json['message'])
 
    def test_period_zero_means_no_period(self):
        sent = []
 
        def post_packet(lampid, packet):
            sent.append(lampid)
            sent.append(packet)
 
        data = {'color': "#ff00ff", 'period': '0'}
        (json, errcode) = V1API(post_packet).handle(id='lamp3',
                                                    formdata=data)
        self.assertEqual(200, errcode)
        self.assertEqual("'lamp3' updated", json['message'])
        self.assertEqual('lamp3', sent[0])
        self.assertEqual((255, 0, 255), sent[1])
 
    def test_period_empty_means_no_period(self):
        sent = []
 
        def post_packet(lampid, packet):
            sent.append(lampid)
            sent.append(packet)
 
        data = {'color': "#ff00ff", 'period': ''}
        (json, errcode) = V1API(post_packet).handle(id='lamp4',
                                                    formdata=data)
        self.assertEqual(200, errcode)
        self.assertEqual("'lamp4' updated", json['message'])
        self.assertEqual('lamp4', sent[0])
        self.assertEqual((255, 0, 255), sent[1])
 
if __name__ == '__main__':
    unittest.main()